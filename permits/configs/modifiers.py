""" This is a monkey-patching module to silently return custom configs per group.

Often it is not enough to say "if the user's group matches the resource's group, permissions are this way"

We want to be able to say "if a user in the 'staff' group finds a match, permissions are this way."

Semantics are adapted from the chown command, so that:

+rw = add read and write
-x = subtract execute
+w,-x = add write, subtract execute.
"""
import collections

from base import BASE_PERMISSIONS

from visd_staff import VISD_STAFF_PERMISSIONS

CONFIG_MAP = {
    'visd-staff': VISD_STAFF_PERMISSIONS
}

def modify(original,modifier):
    """ Accepts a single-digit original and a modifier string. Returns a new digit.

    >>> print modify(2,'+r')
    6

    >>> print modify(5,'-rx')
    0

    >>> print modify(2,'+rx,-w')
    5

    """
    original = int(original)
    modifiers = modifier.split(',')
    for clause in modifiers:
        bitsum = 0
        direction = clause[0]
        for term in list(clause[1:]):
            bitsum = bitsum|{'r':4,'w':2,'x':1}[term]
        if direction == "-":
            original = original&~bitsum
        elif direction == "+":
            original = original|bitsum
    return original

def group_of(config):
    """ We're going to strip away all but the group permissions and return the new dictionary.
    """
    for key in config:
        if hasattr(config[key],'__iter__'):
            config[key] = group_of(config[key].copy())
        else:
            config[key] = config[key][-2]
    return config

def modify_config(old_config,modifier):
    """ Walks through two dictionaries comparing them and adding and calling modify() as needed.

    """
    for key in modifier.keys():
        if key in old_config.keys():
            if hasattr(modifier[key],'__iter__'):
                old_config[key] = modify_config(old_config[key],modifier[key])
            else:
                old_config[key] = modify(old_config[key],modifier[key])
        # else:
        #     old_config[key] = modify(0,modifier[key])
    return old_config


    # for key in old_config.keys():
    #     if key in modifier.keys():
    #         if hasattr(old_config[key],'__iter__'):
    #             old_config[key] = modify_config(old_config[key],modifier[key])
    #         else:
    #             old_config[key] = modify(old_config[key][-2], modifier[key])
    return old_config

def base_config(user_group):
    # mod_config = CONFIG_MAP.get(user_group)
    new_base = BASE_PERMISSIONS.copy()
    # if mod_config:
    #     print 'I can change by that one!'
    #     new_base = modify_config(new_base,mod_config)
    return new_base

if __name__ == '__main__':
    import doctest
    doctest.testmod()