from configs.base import BASE_PERMISSIONS as PERMISSIONS

TEST_DICT = {'skillsets': {
    'fields':
            {'title': '0640',
             'short_description': '0640',
             'long_description': '0640',
             # 'owner': '0640',
             # 'group': '0600',
             'slug': '0400',
             'created_at': '0000',
             'challenges': '0755'},
    'methods':
            {'PUT': '0500',
             'GET': '0555',
             'DELETE': '0500'}
}}


def get_child_groups(group):
    """ Ladies and gentlemen, the dumbest way in history to maintain this information.

    But someday I'll eat my vitamins and implement an rb-tree or something.
    """
    return {
        'admin': ['visd-staff', 'visd-user', 'visd-guest', 'guest'],
        'visd-staff': ['visd-user', 'visd-guest', 'guest'],
        'visd-user': ['visd-guest', 'guest'],
        'visd-guest': ['guest'],
        'guest': []
    }[group]

""" These next two methods can probably be made more effecient, which
would help at runtime.
"""


def can(whom, method, pcode):
    """Accepts a user type, a method and the string version of an octal
    permissions code.

    Returns Boolean.

    >>> print can('group','write','0761')
    True

    >>> print can('world','execute','0640')
    False

    """
    p = permissions_digit_for(whom, pcode)
    result = {
        'execute': 1,
        'write': 2,
        'read': 4
    }[method] & p
    return result and True or False


def permissions_digit_for(type, pcode):
    """ Isolates the number for a group. Accepts the string version of an octal
    permissions code.

    >>> print permissions_digit_for('world','0735')
    5

    >>> print permissions_digit_for('owner','0644')
    6
    """
    return int(dict(zip(['owner', 'group', 'world'], list(pcode[1:])))[type])
    # result = {
    #     'world': lambda x: x[-1],
    #     'group': lambda x: x[-2],
    #     'owner': lambda x: x[-3]
    # }[type](pcode)
    # return int(result)


def can_via(resource, method, access_level, parent_permissions):
    # Accepts the permissions portion of a parent, which must be specified in
    # the calling function.
    pcode = parent_permissions['fields'].get(resource)
    modifier = {
        'read': 4,
        'write': 2,
        'execute': 1
    }[method]
    if pcode:
        return permissions_digit_for(access_level, pcode) & modifier and True or False
    else:
        return False


def permitted_set(dictionary, whom, method):
    """ Accepts a dictionary of permissions and returns a list of keys
    that meet that permission.

    >>> print permitted_set({'title':'0735','nerve':'0745','water':'0663'},'group','write')
    ['water', 'title']

    """
    return [k for k in dictionary.keys() if can(whom, method, dictionary[k])]


def reduce_permissions_dictionary_to(user_type, dictionary):
    """Takes a given permissions dictionary and returns one as seen by just one user.
    """
    new_dict = dictionary.copy()
    for k, v in dictionary.items():
        if hasattr(v, '__iter__'):
            new_dict[k] = reduce_permissions_dictionary_to(user_type, v)
        else:
            new_dict[k] = permissions_digit_for(user_type, v)
    return new_dict


def reduced_for(user_type, resource):
    """A convenience wrapper to isolate the permission bits per resource/user.
    """
    return reduce_permissions_dictionary_to(user_type, PERMISSIONS[resource])


def isolated_permissions_of(resource, user_type):
    """ Returns the single relevant permission digit for a given resource in BASE_RESOURCES.
    """
    return [(k, permissions_digit_for(user_type, v))
            for k, v in PERMISSIONS[resource]['fields'].iteritems()]


def scope_allows_collection(resource, user_type, permissions):
    """ Given the resource whose collection we want to see, the user type,
    and the permissions fragment of the enclosing scope,
    what methods are allowed? Returns a list.

    We assume the execute bit is on, or you wouldn't be asking.
    """
    pdigit = permissions_digit_for(user_type, permissions['fields'][resource])
    results = []
    if pdigit & 4:
        results.append('GET')
    if pdigit & 2:
        results.append('POST')
    return results


def scope_allows_instance(user_type, permissions):
    """ Returns a list of the methods that can be performed on an instance for user of a given type.
    """
    results = []
    for m, v in permissions['methods'].iteritems():
        pdigit = permissions_digit_for(user_type, v)
        if pdigit & 1:
            results.append(m)
    return results

# def field_permissions_digit_for(resource,field):


def fields_permitted_to(user_type, method, resource):
    """ Scans the attributes of the resource and returns a list of the ones 
    available to this user.

    User types: ['owner','group','world'].
    Methods: ['read','write','execute']
    Resource: Whichever.

    This comes after an initial check for access to the resource.
    """
    field_permissions = config_of(resource)['fields']
    return permitted_set(field_permissions, user_type, method)


# def class_permitted_to(user_type,method,resource):
#     """ We want to know if the user has access of this type to the resource in general.

#     Returns Boolean.
#     """
#     resource_permissions = config_of(resource)['permissions']['class']
#     return can(user_type,method,resource_permissions)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
