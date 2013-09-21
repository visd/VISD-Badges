"""
The job of these methods is to contruct a dictionary.
"""
import logging

from django.forms.models import modelform_factory
from django.core.urlresolvers import reverse

from permits import methods as permit
from permits.configs.modifiers import full_config, narrow_config

from badges.resource_configs import reverbose

import helpers as help
from utils import and_list

logger = logging.getLogger(__name__)

VIEW_TRAVERSE_DEPTH = 2


def put_instance(resource=None, resource_id=None,
                 user=None, config=None):
    """ Returns an okay signal.
    """
    # get an instance from model + id.
    # new_resource = form.save(commit=False)
    pass


def get_delete_form(instance, warning=None):
    """ Right away, a button for delete/cancel.
    Then, on clicking the form, perhaps a warning.
    """
    return {'target': {
        'url': instance.url,
        'method': 'DELETE',
        'form': form
    }}


def delete_instance(instance=None, confirm=False):
    """ We'll use the handler to look for a querystring of ?confirm=True.
    We'll also use the delete form to prepare the user for the delete that's
    to come. The user will, on confirming, click on a button that sends
    the all_clear.
    """
    if not confirm:
        child_resources = [rel.get_accessor_name()
                           for rel in instance._meta.get_all_related_objects()]
        if child_resources:
            child_warnings = and_list(child_resources)
            return 'Delete this and all its %s?' % child_warnings
            # Resend a delete form with an alert with a button
            # that links to [:url]?confirm=True DELETE
        else:
            return "Nobody depends on you -- off you go!"
    return "I'll delete you!"
    # instance.delete()


def get_instance(parent=None, parent_id=None,
                 resource=None, instance=None,
                 config=None,
                 user=None, depth=0):
    """ Handles instances. Returns a dictionary of:
        - metadata about the instance;
        - the fields the user is entitled to GET,
        - relations (related resources)

        If the method for any relation is anything but GET
        we don't recurse into it.

        Note that the config has been helpfully pre-tapered down to
        just a single bit for each field and method. So at this level,
        we don't 'know' if the user is owner, group, world and what
        group. Doesn't matter, just do your work, you function.

        Some day, when we're not relying on Django model/instance methods,
        we can pass dictionaries around instead of instances and be, perhaps,
        more efficient with the database.
        Someday.
    """
    allowed = permit.allowed_methods_of(config[resource]['methods'])['allowed']

    # If we called this directly, we want to remove a redundant 'GET'
    # from the list of methods we'll call to the user.
    if not depth:
        allowed.remove('GET')
    # Even an empty set will return this:
    result = {'meta': {}, 'fields': {}, 'relations': {}}
    parent_url = parent and '/%s/%s' % (parent, parent_id) or ''

    # We now remake the config from the user.
    config = help.instance_permissions(user, instance)
    result['meta'] = {'url': '%s%s' % (parent_url, instance.url),
                      'methods': allowed,
                      'tagged_with': [resource],
                      'resource': resource}

    # Now we sort the config into the kind of dictionary we are looking
    # for:
    viewmap = help.viewmap_of(config[resource])

    # And now, the "I'd like to thank my parents" clause.
    # There are two reasons why we might stuff a link to the parent in this dictionary.
    # One is that this is exactly the resource asked for in the user's
    # request. The other is that the instance's parent is not the parent
    # sent to this function.
    if instance.parent_instance:
        parent_resource = instance.parent_instance._meta.verbose_name_plural
        if (not depth) or (parent_resource != parent):
            result['meta']['parent'] = {'resource': parent_resource,
                                        'title': str(instance.parent_instance),
                                        'url': instance.parent_instance.url
                                        }
            viewmap['traversals'] = [
                t for t in viewmap['traversals'] if t['resource'] != parent_resource
            ]
    result['fields'] = {f: getattr(instance, f) for f in viewmap['fields']['read']}
    # Now we add the traversables and, if we have more to go, fire off a
    # call for each one:
    forward = help.valid_traversals(resource, config)
    for t in viewmap['traversals']:
        if 'GET' in t['methods']:
            target_resource = t['resource']
            is_collection = target_resource in forward['many'].keys()
            if VIEW_TRAVERSE_DEPTH - depth:
                if is_collection:
                    opts = {'parent': resource,
                            'parent_id': instance.pk,
                            'resource': target_resource,
                            'user': user,
                            'config': config,
                            'depth': depth + 1
                            }
                    relation = get_collection(**opts)
                else:
                    target_instance = getattr(instance, target_resource)
                    opts = {'resource': reverbose(target_resource),
                            'instance': target_instance,
                            'user': user,
                            'config': config,
                            'depth': depth + 1
                            }
                    relation = get_instance(**opts)
            else:
                # if we have no further loops to do, we'll just put a link to
                # the traversal.
                target = getattr(instance, target_resource)
                if is_collection:
                    relation = {'meta':
                                {'url': target.url(),
                                 'title': str(target),
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
                       config=None, parent_instance=None,
                       user=None, request=None):
    this_model = help.model_for(resource)
    db_columns = help.db_columns_of(this_model)
    # We use this, and the config, to find out which fields on the model this user is
    # permitted to create.
    # Whatever was submitted in the request.POST gets filtered through this.
    write_fields = help.help.sorted_fields_of(
        config['fields'])['fields']['write']
    permitted_fields = list(set(request.POST) &
                            set(write_fields) &
                            set(db_columns))
    # And now, the permitted and user-supplied dictionary:
    values = {k: request.POST[k] for k in permitted_fields}
    # Now we're going to extend the set of fields, because most models will need
    # a user, a group and a parent.
    extensions = []

    # Someday put this next, ugly chunk of code into a loop, and perhaps figure
    # the values outside this method, in a config somewhere.

    if 'user_id' in db_columns:
        values['user_id'] = user.pk
        extensions.append('user_id')
    if 'group_id' in db_columns:
        values['group_id'] = user.status_over(
            parent and getattr(parent_instance, 'group')
            or
            NestedGroup.objects.get(name=settings.INDEX_GROUP))
        extensions.append('group_id')

    # If this new resource needs a parent, let's use the one in the URL.
    # This is assuming we've screened for validity -- we won't get here
    # without all our sanity checks in place.
    p = help.parent_of(resource)
    if p:
        pid = "%s_id" % p
        values[pid] = parent_id
        extensions.append(pid)

    permitted_fields.extend(extensions)

    form = modelform_factory(this_model, fields=permitted_fields)(values)
    opts = {'parent': parent,
            'parent_id': parent_id,
            'resource': resource,
            'user': user,
            'user': user_role,
            'config': config,
            'depth': 0}
    if form.is_valid():
        new_inst = form.save(commit=False)
        # Now we need to sneak in a few more values.

        # Success! Now show the page this belongs on.
        return (True, get_collection(**opts))
    else:
        opts['form'] = form
        return (False, get_post_form(**opts))


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
                  depth=0, form=None):
    """ Returns a dictionary with:
        a form for posting one of this resource, and
        a target url/method for the form.

        We're already checked, and the user is allowed to post one of these.
    """
    if form is None:
        # The user is going to be the owner of this resource.
        this_config = permit.reduce_permissions_dictionary_to('owner', config)

        formfields = help.sorted_fields_of(
            this_config[resource]['fields'])['fields']
        # We only want a form for the fields the owner can read and write.
        userfields = tuple(set(formfields['read']) & set(formfields['write']))

        # Now we create the form.
        this_model = help.model_for(resource)
        form = modelform_factory(this_model, fields=userfields)()

    result = {
        'target': {
            'url': reverse('newviews:parsed-url',
                           kwargs={'parent': parent,
                                   'parent_id': parent_id,
                                   'resource': resource}),
            'method': 'POST',
            'form': form
        }
    }
    return result


def get_collection(parent=None, parent_id=None, resource=None,
                   user=None, config=None,
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
    allowed = permit.methods_for_traversal(parent or 'index', resource, config)
    if not depth:
        # Since we're already GETting this, no need to offer it to the client
        # again.
        allowed.remove('GET')

    this_model = help.model_for(resource)
    # We get to use the model's manager directly if it's the root,
    # or if there is a parent we use the parent's manager.
    if parent:
        # And now a bit of magic naming. We expect the verbose name of the resource
        # to be an attribute of the parent model.
        parent_model = help.model_for(parent)
        parent_inst = parent_model.objects.get(pk=parent_id)
        collection = getattr(parent_inst, resource)
    else:
        collection = this_model.collection

    # Now we need our query filter.
    q = help.build_Q_set(user, resource)

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
        # We don't retrieve collection.all() here. We have to figure:
        logger.info('q = %s' % str(q))
        if q:
            instances = collection.filter(q).all()
        else:
            instances = collection.all()
        logger.info('The query was = %s' % str(instances.query))
        result['objects'] = [get_instance(resource=resource, instance=inst,
                                          parent=parent, parent_id=parent_id,
                                          user=user,
                                          config=help.instance_permissions(
                                              user, inst),
                                          depth=depth + 1)
                             for inst in instances]

    return result

if __name__ == '__main__':
    import doctest
    doctest.testmod()
