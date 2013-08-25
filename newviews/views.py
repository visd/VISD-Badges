import json

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse

from permits.configs.modifiers import base_config
from permits import methods as permit
import methods

def handler(request, parent=None, parent_id=None, resource=None, resource_id=None):
    """Our job is to thoroughly screen the request so we can hand it to our methods freely.
    This way the methods can recurse without wasting clock cycles and database hits doing these checks.
    """
    # To do:
    # We need to handle misformed requests like:
    # /skillsets/67/challenges/8/entries
    # by reducing to:
    # /challenges/8/entries
    # or:
    # /skillsets/67/challenges/8/entries/34
    # by reducing to:
    # /entries/34

    # We painstakingly compute our user's highest security group.
    # For now we'll use a stub.
    user_top_group = 'visd-user'
    
    # We send off for a config conditioned by this group.
    permissions = base_config(user_top_group)

    # Our easiest check:
    if not resource in permissions:
        return 'No such resource exists: %s' % resource
    
    # urls such as "/foo" get rewritten to "index/1/foo"
    if not parent and not(resource=='index'):
        parent="index"
        parent_id=1
    
    # Sneaky, but we must check:
    if parent == "index" and not parent_id == 1:
        parent_id=1

    if not parent in permissions:
        return "Missing resource: %s" % parent
    
    # The parent scope must allow us to traverse to the resource.
    # First we must see if the parent's config even includes the resource.
    parent_p = permissions[parent]['fields'].get(resource)
    if not parent_p:
        return "There's no link from %s to %s." % (parent, resource)

    # Alright, now a database query to see if the parent_resource exists.
    if parent is not "index":
        try:
            parent_model = methods.model_for(parent)
            parent_instance = parent_model.objects.get(pk=parent_id)
        except ObjectDoesNotExist:
            return "%s/%s does not exist." % (parent,parent_id)
    else:
        parent_instance=False

    # Now we'll work out the owner's role vs. this parent instance or the resource.
    # E.g., is this 'owner','group', or 'world'?

    # if not request.user.is_authenticated():
        # user_role = 'world'
    # elif parent is not "index":
        # parent_inst = model_for(parent).objects.get(pk=parent_id)
        # user_role = user_role_for(parent_inst, request.user)
    # else:
    #   user_role = 'group'

    # For now:
    user_role = 'group'

    # The execute bit need to be on.
    if not permit.permissions_digit_for(user_role, parent_p)&1:
        return 'Not legal to traverse from %s to a %s' % (parent, resource)
    
    # A stub.
    this_method = request.method or 'GET'

    # Now we'll see if the method the user wants is permissible.
    if resource_id:
        allowed = permit.scope_allows_instance(user_role,permissions[resource])
    else:
        allowed = permit.scope_allows_collection(resource,user_role,permissions[parent])
    if not this_method in allowed:
        return "The method %s is not allowed." % this_method

    # Last possibility: the resource does not exist. Check for that.
    if resource_id:
        # We'll use the manager of the resource's model to do the query.
        manager = methods.model_for(resource).objects
        try:
            inst = manager.get(pk=resource_id)
            if request.method == 'GET':
                context = methods.get_instance(resource=resource, instance=inst,
                        user=request.user, user_role=user_role, config=permissions)
            if request.method == 'PUT':
                pass
            if request.method == 'DELETE':
                pass
        except ObjectDoesNotExist:
            return 'no such object as %s/%s' % (resource, resource_id)
    else:
        if request.method == 'GET':
            context = methods.get_collection(parent=parent, parent_id=parent_id, resource=resource,
                user=request.user, user_role=user_role, config=permissions)
        if request.method == 'POST':
            pass
    data = json.dumps(context, sort_keys=True, indent=4)
    return HttpResponse(data,content_type='application/json')
