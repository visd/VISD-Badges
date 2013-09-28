import operator

import logging

from importlib import import_module

from django.db.models import Q

from custom.utils import MemoizeMutable, memoized
from newviews.utils import _figure_role

from permits.configs.modifiers import full_config, narrow_config
from permits import TRAVERSAL_PERMISSIONS

from badges.resource_configs import config_from_verbose
from permits.methods import reduce_permissions_dictionary_to, can,\
_sorted_traversals, TRAVERSAL_CODES

from custom_auth.models import CustomUser, NestedGroup

from settings import INDEX_OWNER, INDEX_GROUP

SITE_OWNER = CustomUser.objects.get(email=INDEX_OWNER)
SITE_GROUP = NestedGroup.objects.get(name=INDEX_GROUP)


@memoized
def model_for(resource):
    model_dict = config_from_verbose(resource)
    resource_model = '.'.join([model_dict['app'], 'models'])
    return getattr(import_module(resource_model), model_dict['model'])


@memoized
def parent_of(resource):
    return config_from_verbose(resource).get('parent')


@memoized
def local_fields_of(this_model):
    return [f.name for f in this_model._meta.local_fields]


@memoized
def db_columns_of(this_model):
    return [f.column for f in this_model._meta.local_fields]


def same_tree(user, instance):
    """ If these two are completely out of scope with each other, return
    False.
    """
    return user.status_over(instance.group) and True or False 


def role_for(user, instance):
    """ Looks up the instance's user/group and compares against the user
    and the user's list of all groups. Then determines if the user is the
    owner, group or world of this instance.
    """
    return _figure_role(
        (instance.user_id, instance.group_id),
        user.id,
        user.all_group_ids
    )


def sorted_traversals(resource=None, config=None):
    """ A resource to look up, and a pre-narrowed config.

    We'll go get the traversal permissions, scope both configs,
    and send them off to the be sorted. The result will have
    the valid traversals for this user sorted into 'one', 'many'
    and 'parent'.
    """

    return _sorted_traversals(
        TRAVERSAL_PERMISSIONS[resource]['fields'],
        config[resource]['fields']
        )



def valid_traversals(from_res, config):
    """ Accepts a narrowed config, tapered just to the permission bits for this user.
    Sorts traversals into those that go to the many side of a relation,
    and those that go to the one side of a relation.
    """
    if from_res == 'index':
        local_fields = []
    else:
        local_fields = local_fields_of(model_for(from_res))
    result = {'one': [], 'many': {}}
    for k, v in config[from_res]['fields'].items():
        if v & 1:
            if k in local_fields:
                result['one'].append(k)
            else:
                methods = []
                if v & 4:
                    methods.append('GET')
                if v & 2:
                    methods.append('POST')
                result['many'][k] = methods
    return result


def build_Q(this_user, user_base_config, these_groups):
    """ This receives:
    a user,
    a config, conditioned by a single top_group,
    a set of groups in the same family tree.
    It is just of a single resource. We're going to build a complex
    Q object with this tool.
    """
    get_bits = user_base_config['methods']['GET']
    logging.info('user_base_config = %s' % user_base_config)
    # First, see if the 'world' can GET this.
    # If so, what's with all this complicated stuff?
    needed_groups = []
    needed_user = []
    if can('world', 'execute', get_bits):
        return ([], [])
    elif can('group', 'execute', get_bits):
        needed_groups.extend(these_groups)
    if can('owner', 'execute', get_bits):
        needed_user.append(this_user)
    return (needed_groups, needed_user)


def build_Q_set(this_user, resource):
    """ Returns all the query filters needed to return only the instance_permissions
    this user is permitted to GET.

    First of all, if 'world' can GET these resources, no filter needed.

    If 'group' can GET these resource, make sure they're in the group.
        OR
    If 'owner' can GET these resources, user=owner
    First of all, if 'world' cannot GET these resources, then look
    only for resources in the user's group and children.

    We need a special case for this one. Users and groups have problems with
    circular relationships.
    """
    q_list = []
    for g in this_user.memberships.all():
        q_list.append(build_Q(
                      this_user,
                      full_config(g)[resource],
                      this_user.memberships.children_and_self_of(g))
                     )
    logging.info('q_list = %s' % q_list)
    f = zip(*q_list)
    logging.info('f = %s' % f)
    groups = f[0][0]
    filters = groups and [Q(group__in=groups)] or []
    if f[1][0] and resource is not 'users':
        filters.append(Q(user=this_user))
    return filters and reduce(operator.or_, filters) or False


def instance_permissions(user, instance=None):
    """ How should this user see this instance? Figure's out the user's status
    compared to the instance, then figures owner/group/world for the user,
    then fires off a new copy of that permissions dictionary for that role.

    If instance is missing, we're talking about this site's group and user as
    figured in the settings.
    """
    if not instance:
        top_group = user.status_over(SITE_GROUP)
        user_role = _figure_role((SITE_OWNER.pk, SITE_GROUP.name), 
                                  user.pk,
                                  user.all_group_ids)
    else:
        top_group = user.status_over(instance.group)
        user_role = role_for(user, instance)
    return narrow_config(top_group and top_group.name)[user_role]


def sorted_fields_of(filtered_config, traversal_fields=None):
    """ Given a set of fields, each one with a permission digit, divide them into
        traversals and attributes.

        Fields get sorted into 'read' and/or 'write'.
        Traversals get sorted into 'POST' and/or 'GET'.
    """
    result = {'fields': {'read': [], 'write': []}, 'traversals': []}
    traversal_fields = traversal_fields or TRAVERSAL_PERMISSIONS

    for k, v in filtered_config.items():
        # odd-numbered permissions are executable.
        t_code = traversal_fields.get(k, None)
        if t_code and t_code[0] in TRAVERSAL_CODES:
            if v & 1:
                available = []
                if v & 2:
                    available.append('POST')
                if v & 4:
                    available.append('GET')
                result['traversals'].append(
                    {'url': k, 'methods': available, 'resource': k})
        else:
            if v & 4:
                result['fields']['read'].append(k)
            if v & 2:
                result['fields']['write'].append(k)
    return result


def viewmap_of(resource, config):
    """Accepts a resource and a dictionary already narrowed to a single digit 
    by user role. It uses the routines above to build a kind of template dictionary.

    This method feels inefficient as written. Improvements welcome. Note, however,
    that it does need to return a dictionary with fields, traversals and methods
    even if they're all empty.
    """
    result = {'fields': {}, 'traversals': [], 'methods': []}
    conf = config[resource]
    sorted = sorted_fields_of(
        conf['fields'],
        TRAVERSAL_PERMISSIONS[resource]['fields'])
    result['fields'] = sorted['fields']
    result['traversals'] = sorted['traversals']
    result['methods'] = conf['methods']
    return result


# slated for removal.
# def hydrate(dictionary, instance, method):
#     """ At a point during the construction of the context, we have a model dictionary
#     that represents what we want from this instance. Now we want to take that instance
#     and fill it up with the real information.
#     """
#     result = {'fields': {}, 'traversals': []}
#     if method == 'GET':
#         for f in dictionary['fields']['read']:
#             result['fields'][f] = getattr(instance, f)
#         for t in dictionary['traversals']:
#             result['traversals'].append(
#                 {'url': getattr(instance, t['url']).url(), 'method': t['method']})
#         return result
