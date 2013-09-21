""" Since the modifications of the configs and their modifiers won't happen,
we shouldn't have to build them at runtime, in memory. Instead we'll ask the
user to now-and-then compile them to disk.
"""
import cPickle as pickle
import pprint

from group_mods import MODS
from base import BASE_PERMISSIONS
import modifiers

from permits import methods

pp = pprint.PrettyPrinter()


def _spread_into_roles(d):
    """Take a fat dictionary and returns three, each one narrowed to
    a specific role.
    """
    return {role:methods.reduce_permissions_dictionary_to(role, d)
            for role in ('owner','group','world')}


def compile_configs():
    """Uses the modifiers per group to generate new permissions dictionaries
    and pickle them.
    """
    new_dict = {'BASE': BASE_PERMISSIONS}
    for mod in MODS:
        new_dict[mod] = modifiers.base_config(mod)
    # Now we have a new fat dictionary for each group.
    # Let's pickle it:
    pickle.dump(new_dict, open('permits/configs/full.py', 'w'))
    # Now let's thin it into user_roles:
    narrow_dicts = {k: _spread_into_roles(v) for k, v in new_dict.items()}

    pickle.dump(narrow_dicts, open('permits/configs/narrow.py', 'w'))
    return (pp.pprint(new_dict), pp.pprint(narrow_dicts))


def get_configs():
    perms = pickle.load(open('permits/configs/full.py', 'r'))

    return perms


def _get_diffs(first, second=None):
    from custom import dictdiffer as differ

    dicts = get_configs()
    return differ.diff(dicts[first], dicts[second])


def diffs(first, second=None):
    second = second or 'BASE'
    result = ['%s: %s=>%s' % (field, values[0], values[1])
              for change, field, values in _get_diffs(first, second)]
    return '\n'.join(result)
