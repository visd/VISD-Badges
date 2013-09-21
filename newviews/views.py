# from pprint import pformat
import pprint
import logging

pp = pprint.PrettyPrinter()
logger = logging.getLogger(__name__)

from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.http import Http404, HttpResponse
from django.shortcuts import render

from permits import methods as permit
from helpers import model_for, valid_traversals, instance_permissions, same_tree

from custom_auth.models import CustomUser, NestedGroup

from badges.resource_configs import RESOURCES

import methods


def handler(request, parent=None, parent_id=None,
            resource=None, resource_id=None):
    """Our job is to thoroughly screen the request so we can hand it
    to our methods freely.
    """
    # Until the day we hook Google's auth into our middleware:
    request.user = CustomUser.objects.all()[1]
    logging.info('User: %s, groups: %s' % (str(request.user), str(request.user.memberships.all())))
    # Are these even in our defined list of resources?
    if resource not in RESOURCES or (parent and parent not in RESOURCES):
        raise Http404

    # Does this parent (if there is one) even exist?
    if parent:
        try:
            parent_inst = model_for(parent).objects.get(pk=parent_id)
        except ObjectDoesNotExist:
            raise Http404
        # We'll see if the parent and child are even in the same family tree.
        if not same_tree(request.user, parent_inst):
            raise Http404
        # We need to see if the user is allowed to GET the parent_inst
        # because we will allow the resource to reveal some
        # information about its parent.

        conf = instance_permissions(request.user, parent_inst)
        if not conf[parent]['methods']['GET'] & 1:
            raise PermissionDenied
    else:
        conf = instance_permissions(request.user)

    # Now let's see if we can go from the parent (or index)
    # to this resource.
    traversals = valid_traversals(parent or 'index', conf)['many']
    if not resource in traversals:
        raise PermissionDenied

    opts = {'resource': resource,
            'user': request.user,
            'parent': parent,
            'parent_id': parent_id,
            'config': conf
            }

    if resource_id:
        try:
            inst = model_for(resource).objects.get(pk=resource_id)
        except ObjectDoesNotExist:
            raise Http404
        if not same_tree(request.user, inst):
            raise Http404
        # Time to retrieve the user's permissions for this instance.
        conf = instance_permissions(request.user, inst)
        logging.info('config for resource %s: %s' % (resource, conf[resource]))
        # Now we find out of a user in this role can do this method to this instance.
        allowed = permit.allowed_methods_of(conf[resource]['methods'])['allowed']
        if not request.method in allowed:
            logger.error('Got resource_id, not allowed from method %s, allowed=%s' %
                (request.method, allowed))
            raise PermissionDenied

        if request.method == 'GET':
            opts['instance'] = inst
            opts['config'] = conf
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
            opts['parent_instance'] = parent and parent_inst or None
            post_result = methods.post_to_collection(**opts)
            # post_result sends a tuple of (True/False, context).
            template = post_result[0] and '%s_in_%s.html' % (resource, parent or 'index')\
                or\
                'post_form.html'
            context = post_result[1]       
    return HttpResponse(render(request, template, context), mimetype='text/html')
