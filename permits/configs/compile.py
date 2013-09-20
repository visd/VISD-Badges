""" Since the modifications of the configs and their modifiers won't happen,
we shouldn't have to build them at runtime, in memory. Instead we'll ask the
user to now-and-then compile them to disk.
"""
import cPickle as pickle
import pprint

from group_mods import MODS
from base import BASE_PERMISSIONS
import modifiers


def compile_configs():
    new_dict = {'BASE': BASE_PERMISSIONS}
    for mod in MODS:
        new_dict[mod] = modifiers.base_config(mod)

    pickle.dump(new_dict, open('permits/configs/full.py', 'w'))

    pp = pprint.PrettyPrinter()

    return pp.pprint(new_dict)
