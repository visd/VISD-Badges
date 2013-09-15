# from pprint import pformat

from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.http import Http404, HttpResponse
# from django.template import RequestContext
from django.shortcuts import render

from permits.configs.modifiers import base_config
from permits import methods as permit
from helpers import model_for, local_fields_of, valid_traversals, role_for

from custom_auth.models import CustomUser, NestedGroup

import methods


def handler(request, parent=None, parent_id=None, resource=None, resource_id=None, verb=None):
    """Our job is to thoroughly screen the request so we can hand it to our methods freely.
    This way the methods can recurse without wasting clock cycles and database hits doing these checks.
    """
    # We painstakingly compute our user's highest security group.
    # For now we'll use a stub.

    # On some distant day we'll figure the user from the request. For now:
    user = CustomUser.objects.all()[1]
    user_top_group = 'visd-staff'
    all_user_groups = NestedGroup.collection.all_children_of(user_top_group)

    # We send off for a config conditioned by this group.
    permissions = base_config(user_top_group)

    # Our easiest check:
    if not resource in permissions:
        raise Http404

    if parent and not parent in permissions:
        raise Http404

    # The parent scope must allow us to traverse to the resource.
    # First we must see if the parent's config even includes the resource.
    parent_p = permissions[parent or 'index']['fields'].get(resource)
    if not parent_p:
        raise Http404

    # Alright, now a database query to see if the parent_resource exists.
    if parent:
        if not model_for(parent).objects.filter(pk=parent_id).exists():
            raise Http404

    # Now we'll work out the owner's role vs. this parent instance or the resource.
    # E.g., is this 'owner','group', or 'world'?

    # if not request.user.is_authenticated():
        # user_role = 'world'
    # elif parent:
        # parent_inst = model_for(parent).objects.get(pk=parent_id)
        # user_role = user_role_for(parent_inst, request.user)
    # else:
    #   user_role = 'group'

    # For now:
    user_role = 'group'

    # We need to check if we can traverse in this direction.
    traversals = valid_traversals(parent or 'index',
                                  permit.reduce_permissions_dictionary_to(
                                      user_role, permissions)
                                  )['many']

    if not resource in traversals:
        raise PermissionDenied

    opts = {'resource': resource,
            'user': request.user,
            # 'user_role': user_role,
            'config': permissions,
            'parent': parent,
            'parent_id': parent_id
            }

    # If we have a resource_id, then we don't care if we can get the collection from here.
    # But if we're looking for the collection, then we'll need to check for 'GET' or 'POST'.
    if not resource_id:
        allowed = traversals[resource]
        if not request.method in allowed:
            raise PermissionDenied
    else:
        # This is more complex. We have to seek out this instance, find its user/group
        # and re-figure the user_role.
        manager = model_for(resource).objects
        if not manager.filter(pk=resource_id).exists():
            raise Http404
        inst = manager.get(pk=resource_id)
        user_role = role_for(user, all_user_groups, inst)
        



    # Last possibility: the resource does not exist. Check for that.
    if resource_id:
        # We'll use the manager of the resource's model to do the query.
        manager = model_for(resource).objects
        try:

            if request.method == 'GET':
                opts['instance'] = inst
                requested_form = request.GET.get('form')
                # We may be getting a request for a form, for PUTting or DELETEing.
                # If the user couldn't do this method anyway we just ignore the
                # QueryDict.
                if requested_form == 'edit' and 'PUT' in allowed:
                    context = methods.get_put_form(**opts)
                    template = 'put_form.html'
                if requested_form == 'delete' and 'DELETE' in allowed:
                    context = methods.get_delete_form(**opts)
                    template = 'delete_form.html'
                else:
                    context = methods.get_instance(**opts)
                    template = '%s_detail.html' % resource
            if request.method == 'PUT':
                pass
            if request.method == 'DELETE':
                pass
        except ObjectDoesNotExist:
            raise Http404
    else:
        # We don't travel from "many" to "one." This is, no /chapters/:id/books.
        # Or, in this case, no /entries/:id/challenges.
        # The easiest way is to not let us traverse to the one defined on the
        # resource.

        if request.method == 'GET':
            if request.GET.get('form') == 'create':
                context = methods.get_post_form(**opts)
                template = 'post_form.html'
            else:
                context = methods.get_collection(**opts)
                # magic naming again.
                template = '%s_in_%s.html' % (resource, parent or 'index')
        if request.method == 'POST':
            # We'll either get a redirect or a response containing a new form.
            opts['request'] = request
            post_result = methods.post_to_collection(**opts)
            template = post_result[0] and '%s_in_%s.html' % (resource, parent or 'index')\
                or\
                'post_form.html'
            context = post_result[1]
    return HttpResponse(render(request, template, context), mimetype='text/html')
