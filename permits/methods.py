from collections import defaultdict

from configs.base import BASE_PERMISSIONS as PERMISSIONS

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


def _sorted_traversals(trav_config, user_config):
    """ Made neutral for dependency injection. Use a wrapper
    function to taper the dictionaries down so we are looking
    at the 'fields' of the same resource in both.

    Returns a list of traversals (as identified by trav_config)
    which the user_config says the user can execute.
    """
    new_dict = defaultdict(list)
    terms = {'o': 'one', 'p': 'parent', 'm': 'many'}
    for k, v in trav_config.items():
        if v in terms and user_config.get(k, 0) & 1:
            new_dict[terms[v]].append(k)
    return dict(new_dict)


def methods_for_traversal(from_resource, to_resource, narrowed_config):
    """ Accepts a config narrowed to one user_role (world, group, owner).
    Looks up the from_resource, finds to_resource in 'fields' and declares
    what that bit allows of 'GET' and 'POST'.
    """
    methods = []
    t = narrowed_config[from_resource]['fields'][to_resource]
    if t & 4:
        methods.append('GET')
    if t & 2:
        methods.append('POST')
    return methods


def permissions_digit_for(type, pcode):
    """ Isolates the number for a group. Accepts the string version of an octal
    permissions code.

    >>> print permissions_digit_for('world','0735')
    5

    >>> print permissions_digit_for('owner','0644')
    6
    """
    return int(dict(zip(['owner', 'group', 'world'], list(pcode[1:])))[type])


def traversal_code(pcode):
    """ Pulls the 'm' out of 'm460' and so on. Probably more text than it's worth!
    """
    return pcode[0]


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


def traversal_bits(dictionary):
    """ Identical to above, only returns the traversal bit.
    """
    new_dict = {}
    for k, v in dictionary.items():
        if hasattr(v, '__iter__'):
            new_dict[k] = traversal_bits(v)
        else:
            new_dict[k] = v[0]
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


if __name__ == '__main__':
    import doctest
    doctest.testmod()
