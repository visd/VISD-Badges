"""
The job of these methods is to contruct a dictionary 

Views are constructed from the intersection of the desired fields in the  
"""

from permits import methods as permit
from badges.resource_configs import deverbose
from importlib import import_module
from view_configs.mods import filter_permissions_for

from helpers import memoized

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
    new_dict={}
    for key in modifier.keys():
        if modifier[key].get('omit'):
            new_dict[key] = {k:original_dict[key][k] for k in original_dict[key].keys() if k not in modifier[key]['omit']}
    return new_dict

@memoized
def model_for(resource):
    model_dict = deverbose(resource)
    resource_model = '.'.join([model_dict['app'], 'models'])
    return getattr(import_module(resource_model),model_dict['model'])

def hydrate(dictionary,instance,method):
    """ Uses the dictionary as a manifest for pulling data from the instance.

    "method" is http method.
    """
    result = {'fields':{},'traversals':[]}
    # url = instance.url
    if method == 'GET':
        result['fields'] = [{f:getattr(instance,f) for f in dictionary['fields']['read']}]
        for t in dictionary['traversals']:
            result['traversals'].append({'url':getattr(instance,t['url']).url(),'method':t['method']})
        return result

""" The next two functions use narrow slices of the permissions to generate portions
of the target dictionaries. In other words, these are the functions that translate
permissions in to views.
"""
def sorted_fields_of(filtered_config):
    """ Given a set of fields, each one with a permission digit, divide them into
        traversals and attributes, and filter them into GET/POST traversals
        and READ/WRITE fields.
    """
    result = {'fields':{'read':[],'write':[]},'traversals':[]}
    if filtered_config:
        for k, v in filtered_config.items():
            # odd-numbered permissions are executable.
            if v&1:
                available=[]
                if v&2:
                    available.append('POST')
                if v&4:
                    available.append('GET')
                result['traversals'].append({'url': k,'methods':[available]})
            else:
                if v&4:
                    result['fields']['read'].append(k)
                if v&2:
                    result['fields']['write'].append(k)   
    return result

def allowed_methods_of(method_dict):
    """ Accepts a dictionary, isolated by user type, plucked from the "methods" portion
    of a permissions config.

    >>> test_dict = {'PUT': 1, 'GET': 5, 'DELETE': 0}

    >>> print allowed_methods_of(test_dict)
    {'offered': ['GET'], 'allowed': ['PUT', 'GET']}
    """
    result = {'allowed':[],'offered':[]}
    for method, code in method_dict.iteritems():
        if code&1:
            result['allowed'].append(method)
            if code&4:
                result['offered'].append(method)
    return result

def viewmap_of(resource_config):
    # This accepts a dictionary already narrowed to a single digit by user role.
    # Sends off the fields for sorting.
    result = {'fields':{}, 'traversals':[],'methods':[]}

    if resource_config.get('fields'):
        sorted = sorted_fields_of(resource_config['fields'])
        result['fields'] = sorted['fields']
        result['traversals'] = sorted['traversals']

    if resource_config.get('methods'):
        result['methods'] = (resource_config['methods'])
    return result

def viewmaps_of(resource, depth):
    # retrieves viewmaps and screens them against the depth of the request (0 or less)
    return dict([(level, viewmap_of(resource, level)) for level in ['owner','group','world']])


def put_instance(resource=None, resource_id=None,
                    user=None, config=None):
    """ Returns an okay signal.
    """

def delete_instance(resource=None, resource_id=None):
    """ You heard the nice man, delete it. Clean up after it, too.
    """

def can_traverse(d):
    """ Given a dictionary, returns a list of the items which are traversable.
        (i.e., user can visit and can traverse.)

    >>> print can_traverse({'foo':7,'bar':0})
    ['foo']
    """
    return [k for k,v in d.iteritems() if v&1 and v&4]

def get_instance(resource=None, instance=None, 
                    user=None, user_role=None, config=None,
                    depth=0):
    """ Handles instances. Returns a dictionary of 
        If the method is anything but GET we don't recurse.
        Accepts, among many other parameters, an instance of the given resource type.

        Some day, when we're not relying on Django model/instance methods, we can pass
        dictionaries around instead of instances and be many times more efficient with the database.
        Someday.
    """
    
    allowed = permit.scope_allows_instance(user_role,config[resource])
    if 'GET' in allowed:
        if not depth:
            allowed.remove('GET')
        # Now we have to weigh the user vs. the object to determine the user role
        # For now:    
        user_role = 'group'

        # We narrow the scope of the config to just this resource.
        this_config = config[resource]
        
        # We narrow it by filtering it against the view for the current depth.
        new_config=filter_permissions_for(resource, this_config, depth)
      
        new_config = permit.reduce_permissions_dictionary_to(user_role, new_config)        

        # Even an empty set will return this:
        result = {'meta':{},'fields':{},'traversals':[]}
        result['meta'] = {'url':instance.url,'methods':allowed}

        # Now we sort the config into the kind of dictionary we are looking for:
        viewmap = viewmap_of(new_config)       
        result['fields']={f:getattr(instance,f) for f in viewmap['fields']['read']}
        # Now we add the traversables and, if we have more to go, fire off a call for each one:
        for t in viewmap['traversals']:
            traversal = {'url':getattr(instance,t['url']).url(),'methods':t['methods']}
            # If we still have a ways to go, stuff the next layer into 'preload' on this traversal.
            if VIEW_TRAVERSE_DEPTH-depth:
                if t['url'] in can_traverse(new_config['fields']):
                    traversal['preload'] = get_collection(parent=resource, parent_id=instance.pk, resource=t['url'], 
                                    user=user, user_role=user_role, config=config, depth=depth+1)
            result['traversals'].append(traversal)
        # result = hydrate(viewmap,instance,'GET')
        if not depth:
            result['traversals'].append({'url':'/%s' % resource, 'method':'GET'})
        return result

def post_to_collection(parent=None, parent_id=None, resource=None,
        user=None, config=None):
    pass

def get_collection(parent=None, parent_id=None, resource=None,
          user=None, user_role= None, config=None,
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
    allowed = permit.scope_allows_collection(resource,user_role,config[parent])
    if not depth:
        allowed.remove('GET')

    this_model = model_for(resource)
    # We get to use the model's manager directly if it's the root, or we
    # are at a scope such as /foo/:id/bar/:id, which will return a url of
    # /bar/:id
    if parent == 'index':
        collection = this_model.collection
    else:
        # And now a bit of magic naming. We expect the verbose name of the resource
        # to be an attribute of the parent model.
        parent_model = model_for(parent)
        parent_inst = parent_model.objects.get(pk=parent_id)
        collection = getattr(parent_inst,resource)

    # The following count will only be accurate when we filter collections by owner/group.`
    result={'meta':{'url':collection.url(), 'methods':[m for m in allowed], 'count': collection.count()}}
    if not parent == 'index' and not depth:
        result['traversals'] = ([{'url':parent_inst.url,'method':'GET'},
                                  {'url':parent_model.collection.url(),'method':'GET'}])
    if VIEW_TRAVERSE_DEPTH-depth:
        # now we have to send along a list of ready instances or we're going to clobber the database.
        # We're going to build a Q object so our queryset gets only the ones we're looking for.
        # For now 
        get_flag = None
        result[resource] = [get_instance(resource=resource, instance=inst, 
                                      user=user, user_role=user_role, config=config,
                                      depth=depth+1) 
                         for inst in collection.all()]
    return result

if __name__ == '__main__':
    import doctest
    doctest.testmod()