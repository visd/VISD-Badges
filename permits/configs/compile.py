""" 
This is a monkey-patching module to silently return custom configs per group.

Often it is not enough to say "if the user's group matches the resource's group, permissions are this way"

We want to be able to say "if a user in the 'staff' group finds a match, permissions are this way."

Semantics are adapted from the chown command, so that:

+rw = add read and write
-x = subtract execute
+w,-x = add write, subtract execute.

Since the modifications of the configs and their modifiers won't happen,
we shouldn't have to build them at runtime, in memory. Instead we'll ask the
user to now-and-then compile them to disk.
"""

import cPickle as pickle
import pprint

from group_mods import MODS
from base import BASE_PERMISSIONS

from permits import methods, FULL_PERMISSIONS, NARROW_PERMISSIONS

pp = pprint.PrettyPrinter()


def _spread_into_roles(d):
    """Take a fat dictionary and returns three, each one narrowed to
    a specific role.
    """
    return {role: methods.reduce_permissions_dictionary_to(role, d)
            for role in ('owner', 'group', 'world')}

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


def mod_config(user_group=None):
    """ If we recognize this group, then we'll send out a new modified version of BASE_PERMISSIONS.

    Otherwise, you'll just get BASE_PERMISSIONS.
    """
    if user_group:
        modify_dict = MODS[user_group]
        pre = modify_dict.get('inherits')
        new_base = modify_config(pre and mod_config(pre) or BASE_PERMISSIONS,
                                 modify_dict['values'])
        return new_base
    else:
        return BASE_PERMISSIONS


def compile_configs():
    """Uses the modifiers per group to generate new permissions dictionaries
    and pickle them.
    """
    new_dict = {'BASE': BASE_PERMISSIONS}
    for mod in MODS:
        new_dict[mod] = mod_config(mod)
    # Now we have a new fat dictionary for each group.
    # Let's pickle it:
    pickle.dump(new_dict, open('permits/configs/full.py', 'w'))
    # Now let's thin it into user_roles:
    narrow_dicts = {k: _spread_into_roles(v) for k, v in new_dict.items()}

    pickle.dump(narrow_dicts, open('permits/configs/narrow.py', 'w'))
    return (pp.pprint(new_dict), pp.pprint(narrow_dicts))


def get_full_configs():
    return FULL_PERMISSIONS


def get_narrow_configs():
    return NARROW_PERMISSIONS


def _get_diffs(first, second=None):
    from custom import dictdiffer as differ

    return differ.diff(FULL_PERMISSIONS[first], FULL_PERMISSIONS[second])


def diffs(first, second=None):
    second = second or 'BASE'
    result = ['%s: %s=>%s' % (field, values[0], values[1])
              for change, field, values in _get_diffs(first, second)]
    return '\n'.join(result)
