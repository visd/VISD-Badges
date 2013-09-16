# from pprint import pformat

from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.http import Http404, HttpResponse
# from django.template import RequestContext
from django.shortcuts import render

from permits.configs.modifiers import base_config
from permits import methods as permit
from helpers import model_for, local_fields_of, valid_traversals, role_for

from custom_auth.models import CustomUser, NestedGroup

from resource_configs import RESOURCES

import methods


def handler(request, parent=None, parent_id=None,
            resource=None, resource_id=None, verb=None):
    """Our job is to thoroughly screen the request so we can hand it
    to our methods freely.
    """
    if resource not in RESOURCES or (parent and parent not in RESOURCES):
        raise Http404

    if parent:
        try:
            parent_inst = model_for(parent).objects.get(pk=parent_id)
        except ObjectDoesNotExist:
            raise Http404
        
        parent_p = permissions[parent or 'index']['fields'].get(resource)
        if not parent_p:
            raise Http404

    if resource_id:
        if not model_for(resource).objects.filter(pk=resource_id).exists():
            raise Http404

    # The parent scope must allow us to traverse to the resource.
    # First we must see if the parent's config even includes the resource.


    # We need to check if we can traverse in this direction.
    traversals = valid_traversals(parent or 'index',
                                  permit.reduce_permissions_dictionary_to(
                                      user_role, permissions)
                                  )['many']
    if not resource in traversals:
        raise PermissionDenied

    opts = {'resource': resource,
            'user': request.user,
            'config': permissions,
            'parent': parent,
            'parent_id': parent_id
            }

    user = CustomUser.objects.all()[2]
    user_top_group = user.status_over('visd-guest')

    # We send off for a config conditioned by this group.
    permissions = base_config(user_top_group)


    if resource_id:
        # Now we have to figure out the user's role for this resource.
        try:
            inst = model_for(resource).object.get(pk=resource_id)
        except ObjectDoesNotExist:
            raise Http404
        user_role = role_for(user, inst)

        # Now we find out of a user in this role can do this method to this instance.


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
    else:
        allowed = traversals[resource]
        if not request.method in allowed:
            raise PermissionDenied
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



    
