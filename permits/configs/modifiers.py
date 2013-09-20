""" This is a monkey-patching module to silently return custom configs per group.

Often it is not enough to say "if the user's group matches the resource's group, permissions are this way"

We want to be able to say "if a user in the 'staff' group finds a match, permissions are this way."

Semantics are adapted from the chown command, so that:

+rw = add read and write
-x = subtract execute
+w,-x = add write, subtract execute.
"""

from group_mods import MODS

from base import BASE_PERMISSIONS

CONFIG_MAP = {
    'visd-staff': 'visd-staff',
    'admin': 'admin'
}


def modify(original, modifier):
    """ Accepts a single-digit original and a modifier string. Returns a string.

    >>> print modify(2,'+r')
    6

    >>> print modify(5,'-rx')
    0

    >>> print modify(2,'+rx,-w')
    5

    """
    result = int(original)
    modifiers = modifier.split(',')
    for clause in modifiers:
        bitsum = 0
        direction = clause[0]
        for term in list(clause[1:]):
            bitsum = bitsum | {'r': 4, 'w': 2, 'x': 1}[term]
        if direction == "-":
            result = result & ~bitsum
        elif direction == "+":
            result = result | bitsum
    return str(result)


def group_of(config):
    """ We're going to strip away all but the group permissions and return the new dictionary.

    SLATED FOR REMOVAL.
    """
    result_dict = {}
    for key, item in config.items():
        if hasattr(item, '__iter__'):
            result_dict[key] = group_of(item)
        else:
            result_dict[key] = item[-2]
    return result_dict


def replace_group(original_group, modifier):
    """
    >>> print replace_group('0700','+rwx')
    0770

    >>> print replace_group('0520','+r,-w')
    0540
    """
    li = list(original_group)
    li[-2] = modify(li[-2], modifier)
    return ''.join(li)


def modify_config(old_config, modifier):
    """ Walks through two dictionaries comparing them and adding and calling modify() as needed.

    """
    result = {}
    for key, item in old_config.items():
        if key in modifier.keys():
            if hasattr(modifier[key], '__iter__'):
                result[key] = modify_config(old_config[key], modifier[key])
            else:
                result[key] = replace_group(old_config[key], modifier[key])
        else:
            result[key] = item
    return result


def base_config(user_group=None):
    """ If we recognize this group, then we'll send out a new modified version of BASE_PERMISSIONS.

    Otherwise, you'll just get BASE_PERMISSIONS.
    """
    group_listed = user_group and CONFIG_MAP.get(user_group) or None
    if group_listed:
        mod_config = MODS[group_listed]
        pre = mod_config.get('inherits')
        new_base = modify_config(pre and base_config(pre) or BASE_PERMISSIONS,
                                 mod_config['values'])
        return new_base
    else:
        return BASE_PERMISSIONS

if __name__ == '__main__':
    import doctest
    doctest.testmod()
