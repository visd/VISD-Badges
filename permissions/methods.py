from configs import BASE_PERMISSIONS

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
    pcode = permissions_for(whom,pcode)
    result = {
        'execute': lambda x: x[-1],
        'write': lambda x: x[-2],
        'read': lambda x: x[-3]
    }[method]('{0:03b}'.format(pcode))
    return int(result) and True or False


def permissions_for(type, pcode):
    """ Isolates the number for a group. Accepts the string version of an octal 
    permissions code.

    >>> print permissions_for('world','0735')
    5

    >>> print permissions_for('owner','0644')
    6
    """
    return int(dict(zip(['owner','group','world'],list(pcode[1:])))[type])
    # result = {
    #     'world': lambda x: x[-1],
    #     'group': lambda x: x[-2],
    #     'owner': lambda x: x[-3]
    # }[type](pcode)
    # return int(result)


def permitted_set(dictionary,whom,method):
    """ Accepts a dictionary of permissions and returns a list of keys
    that meet that permission.

    >>> print permitted_set({'title':'0735','nerve':'0745','water':'0663'},'group','write')
    ['water', 'title']

    """
    return [k for k in dictionary.keys() if can(whom,method,dictionary[k])]


def config_of(resource):
    """ Returns the fields associated with a given resource in BASE_RESOURCES.
    """

    return BASE_PERMISSIONS[resource]


def fields_permitted_to(user_type,method,resource):
    """ Scans the attributes of the resource and returns a list of the ones 
    available to this user.

    User types: ['owner','group','world'].
    Methods: ['read','write','execute']
    Resource: Whichever.

    This comes after an initial check for access to the resource.
    """
    field_permissions = config_of(resource)['fields']
    return permitted_set(field_permissions,user_type,method)


# def class_permitted_to(user_type,method,resource):
#     """ We want to know if the user has access of this type to the resource in general.

#     Returns Boolean.
#     """
#     resource_permissions = config_of(resource)['permissions']['class']
#     return can(user_type,method,resource_permissions)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
 