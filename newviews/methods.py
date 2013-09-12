"""
The job of these methods is to contruct a dictionary

Views are constructed from the intersection of the desired fields in the
"""
import logging

from django.forms.models import modelform_factory

from permits import methods as permit
from badges.resource_configs import deverbose, reverbose
from importlib import import_module
from view_configs.mods import filter_permissions_for

from helpers import memoized

logger = logging.getLogger(__name__)

VIEW_TRAVERSE_DEPTH = 2

# METHODS_MAP = {
#     'GET': 'read',
#     'PUT': 'write',
#     'DELETE': 'write',
#     'POST': 'write'
# }


def access_as(user_id, user_groups, res_owner, res_group):
    """ Given this user's id, a list of user's groups, and this resource's owner/group,
    in what role (owner, group, world) should this user view this resource?

    >>>print access_as(11,[2,4,9],34,4)
    'group'

    >>>print access_as(11,[2,4,9],11,9)
    'owner'

    >>>print access_as(11,[2,4,9],34,13)
    'world'
    """
    if user_id == res_owner:
        return 'owner'
    elif res_group in user_groups:
        return 'group'
    else:
        return 'world'


def condition_view(original_dict, modifier):
    """ Takes a dictionary of permissions and omits the keys in corresponding lists
        whose key is "omit."
    """
    new_dict = {}
    for key in modifier.keys():
        if modifier[key].get('omit'):
            new_dict[key] = {k: original_dict[key][k] for k in original_dict[key].keys()
                             if k not in modifier[key]['omit']}
    return new_dict


@memoized
def model_for(resource):
    model_dict = deverbose(resource)
    resource_model = '.'.join([model_dict['app'], 'models'])
    return getattr(import_module(resource_model), model_dict['model'])


""" The next two functions use narrow slices of the permissions to generate portions
of the target dictionaries. In other words, these are the functions that translate
permissions in to views.
"""


def sorted_fields_of(filtered_config):
    """ Given a set of fields, each one with a permission digit, divide them into
        traversals and attributes.

        Fields get sorted into 'read' and/or 'write'.
        Traversals get sorted into 'POST' and/or 'GET'.
    """
    result = {'fields': {'read': [], 'write': []}, 'traversals': []}
    if filtered_config:
        for k, v in filtered_config.items():
            # odd-numbered permissions are executable.
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


def allowed_methods_of(method_dict):
    """ Accepts a dictionary, isolated by user type, plucked from the "methods" portion
    of a permissions config. Note that these are methods on the instance: We can
    see it, change it, delete it.

    >>> test_dict = {'PUT': 1, 'GET': 5, 'DELETE': 0}

    >>> print allowed_methods_of(test_dict)
    {'offered': ['GET'], 'allowed': ['PUT', 'GET']}
    """
    result = {'allowed': [], 'offered': []}
    for method, code in method_dict.iteritems():
        if code & 1:
            result['allowed'].append(method)
            # No point offering a method that isn't allowed -- and so we nest.
            if code & 4:
                result['offered'].append(method)
    return result


def viewmap_of(resource_config):
    """This accepts a dictionary already narrowed to a single digit by user role
    and limited to one resource. It uses the routines above to build a
    dehydrated dictionary.

    This method feels inefficient as written. Improvements welcome. Note, however,
    that it does need to return a dictionary with fields, traversals and methods
    even if they're all empty.
    """
    result = {'fields': {}, 'traversals': [], 'methods': []}

    if resource_config.get('fields'):
        sorted = sorted_fields_of(resource_config['fields'])
        result['fields'] = sorted['fields']
        result['traversals'] = sorted['traversals']

    if resource_config.get('methods'):
        result['methods'] = (resource_config['methods'])
    return result


def viewmaps_of(resource, depth):
    """ Slated for removal.
    """
    return dict([(level, viewmap_of(resource, level)) for level in ['owner', 'group', 'world']])


def hydrate(dictionary, instance, method):
    """ At a point during the construction of the context, we have a model dictionary
    that represents what we want from this instance. Now we want to take that instance
    and fill it up with the real information.

    Think of this as a sort of inner equivalent of a Django model instantiating itself
    from the database. Or think of the diner's ticket finally reaching the chef, who
    proceeds to cook the meal.

    First we'll lay out a dictionary of fields and traversals, then use the

    "method" is http method.
    """
    result = {'fields': {}, 'traversals': []}
    if method == 'GET':
        for f in dictionary['fields']['read']:
            result['fields'][f] = getattr(instance, f)
        for t in dictionary['traversals']:
            result['traversals'].append(
                {'url': getattr(instance, t['url']).url(), 'method': t['method']})
        return result


def put_instance(resource=None, resource_id=None,
                 user=None, config=None):
    """ Returns an okay signal.
    """
    # get an instance from model + id.
    # new_resource = form.save(commit=False)


def delete_instance(resource=None, resource_id=None):
    """ You heard the nice man, delete it. Clean up after it, too.
    """


def manager_from(parent, parent_id, resource):
    """ A convenience; returns the parent's related manager for this resource.
    """
    return getattr(model_for(parent).objects.get(pk=parent_id), resource)


def can_traverse(d):
    """ Pass in a shallow dictionary of fields, along with their permission codes.
    Returns which ones the users can traverse. This is to control the
    nested retrieval of resources. It doesn't determine which ones the client
    sees as available. It's possible to recurse through resources via a collection
    the user cannot GET directly

    >>> print can_traverse({'foo':7,'bar':0,'baz':1})
    ['foo','baz']
    """
    return [k for k, v in d.iteritems() if v & 1]

""" An optimization:

From the model class, find the database fields.

Delay retrieving the instance until we know what fields we'll retrieve, then

(manager).only(*fields)
"""

def get_instance(parent=None, parent_id=None,
                 resource=None, instance=None,
                 user=None, user_role=None, config=None,
                 depth=0):
    """ Handles instances. Returns a dictionary of fields, traversals and
        allowed methods for the user to perform on the instance.

        Think of a url such as '/foo/134'. This function would receive
        'resource="foo",instance = <fooinstance> and so on.'

        If the method is anything but GET we don't recurse.
        Accepts, among many other parameters, an instance of the given resource type.

        Some day, when we're not relying on Django model/instance methods, we can pass
        dictionaries around instead of instances and be many times more efficient 
        with the database.
        Someday.
    """

    # Now we have to weigh the user vs. the object to determine the user role
    # For now:
    user_role = 'group'

    # We narrow the scope of the config to just this resource.
    this_config = config[resource]

    # We narrow it by filtering it against the view for the current depth.
    narrow_config = filter_permissions_for(resource, this_config, depth)

    allowed = permit.scope_allows_instance(user_role, narrow_config)
    if 'GET' in allowed:
        # If we called this directly, we want to remove a redundant 'GET'
        # from the list of methods we'll call to the user.
        if not depth:
            allowed.remove('GET')


        new_config = permit.reduce_permissions_dictionary_to(
            user_role, narrow_config)

        # Even an empty set will return this:
        result = {'meta': {}, 'fields': {}, 'relations': {}}
        parent_url = parent and '/%s/%s' % (parent, parent_id) or ''
        result['meta'] = {'url': '%s%s' % (parent_url, instance.url),
                          'methods': allowed,
                          'tagged_with': [resource],
                          'resource': resource}
        # And now, the "I'd like to thank my parents" clause.
        # There are two reasons why we might stuff a link to the parent in this dictionary.
        # One is that this is exactly the resource asked for in the user's
        # request. The other is that the instance's parent is not the parent
        # sent to this function.
        if instance.parent:
            if (not depth) or (instance.parent._meta.verbose_name_plural != parent):
                result[
                    'meta']['parent'] = {'resource': unicode(instance.parent._meta.verbose_name_plural),
                                         'title': str(instance.parent),
                                         'url': instance.parent.url
                                         }

        # Now we sort the config into the kind of dictionary we are looking
        # for:
        viewmap = viewmap_of(new_config)
        result['fields'] = {f: getattr(instance, f) for f in viewmap['fields']['read']}
        # Now we add the traversables and, if we have more to go, fire off a
        # call for each one:
        # result['traversals'] = viewmap['traversals']
        #  ex: viewmap['traversals']==
        #         [{'methods': ['POST', 'GET'], 'resource': 'user', 'url': 'user'}]
        for t in viewmap['traversals']:
            if 'GET' in t['methods']:
                # target_resource == 'user'
                target_resource = t['resource']
                # What do we get when we access the instance field named the same as the resource?
                target = getattr(instance, target_resource)
                is_collection = target.__class__.__name__ in ('RelatedManager', 'ManyRelatedManager')
                if VIEW_TRAVERSE_DEPTH - depth:
                    opts = {'parent': resource,
                            'parent_id': instance.pk,
                            'resource': target_resource,
                            'user': user,
                            'user_role': user_role,
                            'config': config,
                            'depth': depth + 1}
                    # We're trying to find out if we're looking at a manager or an instance.
                    # Wiser ways of doing this are welcome as this feels a little fluky.
                    if is_collection:
                        relation = get_collection(**opts)
                    else:
                        opts['resource'] = reverbose(target_resource)
                        opts['instance'] = target
                        relation = get_instance(**opts)
                else:
                    # if we have no further loops to do, we'll just put a link to 
                    # the traversal.
                    if is_collection:
                        relation = {'meta':
                                    {'url': target.url(),
                                     'title': str(instance),
                                     'methods': t['methods'],
                                     }
                                    }
                    else:
                        relation = {'meta':
                                     {'url': str(getattr(target, 'url')),
                                      'title': str(target),
                                      'methods': ['GET']
                                     }
                                    }
                result['relations'][target_resource] = relation
        result['depth left'] = VIEW_TRAVERSE_DEPTH - depth
        return result


def post_to_collection(parent=None, parent_id=None, resource=None,
                       user=None, config=None, request=None):
    pass


def get_put_form(parent=None, parent_id=None,
                 resource=None, instance=None,
                 user=None, user_role=None, config=None,
                 depth=0):
    """ Returns a dictionary with a form to PUT this resource. 
    Also includes read-only fields in the dictionary (not in the form).
    Extra-deluxe functionality would determine if the parent was of a different
    sort than the instance's natural parent, and if so would (depending on permissions)
    prefill this adopted parent in the form.
    """
    pass


def get_post_form(parent=None, parent_id=None,
                  resource=None, instance=None,
                  user=None, user_role=None, config=None,
                  depth=0):
    """ Returns a dictionary with:
        a form for posting one of this resource, and
        a target url/method for the form.

        We're already checked, and the user is allowed to post one of these.
    """
    # This one is simple: The user is going to be the owner of this resource.
    this_config = permit.reduce_permissions_dictionary_to('owner', config)
    this_model = model_for(resource)

    formfields = sorted_fields_of(this_config[resource]['fields'])['fields']
    # We only want a form for the fields the owner can read and write.
    userfields = tuple(set(formfields['read']) & set(formfields['write']))

    # We'll need the manager to tell us the url.
    manager = parent and manager_from(parent, parent_id, resource)\
        or\
        this_model.collection

    # Now we create the form.
    form_class = modelform_factory(this_model, fields=userfields)
    result = {'form': form_class()}
    result['target'] = {'url': '%s%s' %
                        (parent and '/%s/%s' % (parent, parent_id) or '',
                         manager.url()),
                        'method': 'POST'
                        }
    return result


def get_collection(parent=None, parent_id=None, resource=None,
                   user=None, user_role=None, config=None,
                   depth=0):
    """ Requires a resource with a parent scope (which may be index if provided
        by the url router). Parent must come with an id.
        We set the depth to track our recursions and condition the views
        (deeper calls generally return less).

        User is a User instance.

        We will only recurse on GET (and perhaps someday OPTIONS), because it is idempotent.

        All the legal checks are in the handler. Once we recurse we assume
        our configuration is only throwing valid responses.
    """
    allowed = permit.scope_allows_collection(resource, user_role, config[parent or 'index'])
    if not depth:
        # Since we're already GETting this, no need to offer it to the client
        # again.
        allowed.remove('GET')

    this_model = model_for(resource)
    # We get to use the model's manager directly if it's the root, or if there is a parent
    # we use the parent's manager.
    if parent:
        # And now a bit of magic naming. We expect the verbose name of the resource
        # to be an attribute of the parent model.
        parent_model = model_for(parent)
        parent_inst = parent_model.objects.get(pk=parent_id)
        collection = getattr(parent_inst, resource)
    else:
        collection = this_model.collection

    # The following count will only be accurate when we filter collections by
    # owner/group.`
    result = {'meta': {
        'resource': resource,
        'url': collection.url(),
        'methods': [m for m in allowed],
        'count': collection.count()
    }
    }
    if parent and not depth:
        result['traversals'] = [{'url': parent_inst.url, 'method': 'GET'}]
    if VIEW_TRAVERSE_DEPTH - depth:
        # If there's any database clobbering going on, this might be the place.
        result['objects'] = [get_instance(resource=resource, instance=inst,
                                          parent=parent, parent_id=parent_id,
                                          user=user, user_role=user_role, config=config,
                                          depth=depth + 1)
                             for inst in collection.all()]
    return result

if __name__ == '__main__':
    import doctest
    doctest.testmod()
