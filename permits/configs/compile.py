""" Since the modifications of the configs and their modifiers won't happen,
we shouldn't have to build them at runtime, in memory. Instead we'll ask the
user to now-and-then compile them to disk.
"""
import cPickle as pickle
import pprint

from group_mods import MODS
from base import BASE_PERMISSIONS
import modifiers

pp = pprint.PrettyPrinter()


def compile_configs():
    new_dict = {'BASE': BASE_PERMISSIONS}
    for mod in MODS:
        new_dict[mod] = modifiers.base_config(mod)

    pickle.dump(new_dict, open('permits/configs/full.py', 'w'))

    return pp.pprint(new_dict)


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
