import collections
import functools
import cPickle
from importlib import import_module

from utils import MemoizeMutable, _figure_role

from badges.resource_configs import config_from_verbose
from permits.configs.modifiers import base_config
from permits.methods import reduce_permissions_dictionary_to


class memoized(object):
    '''Decorator. Caches a function's return value each time it is called.
    If called later with the same arguments, the cached value is returned
    (not reevaluated).
    '''

    def __init__(self, func):
        self.func = func
        self.cache = {}

    def __call__(self, *args):
        if not isinstance(args, collections.Hashable):
            # uncacheable. a list, for instance.
            # better to not cache than blow up.
            return self.func(*args)
        if args in self.cache:
            return self.cache[args]
        else:
            value = self.func(*args)
            self.cache[args] = value
            return value

    def __repr__(self):
        '''Return the function's docstring.'''
        return self.func.__doc__

    def __get__(self, obj, objtype):
        '''Support instance methods.'''
        return functools.partial(self.__call__, obj)


@memoized
def model_for(resource):
    model_dict = config_from_verbose(resource)
    resource_model = '.'.join([model_dict['app'], 'models'])
    return getattr(import_module(resource_model), model_dict['model'])


@memoized
def parent_of(resource):
    return config_from_verbose(resource).get('parent')


@memoized
def local_fields_of(this_model):
    return [f.name for f in this_model._meta.local_fields]


@memoized
def db_columns_of(this_model):
    return [f.column for f in this_model._meta.local_fields]


def role_for(user, instance):
    """ Looks up the instance's user/group and compares against the user
    and the user's list of all groups. Then determines if the user is the
    owner, group or world of this instance.
    """
    return _figure_role(
        (instance.user_id, instance.group_id),
        user.id,
        user.all_membership_ids
    )


@MemoizeMutable
def valid_traversals(from_res, config):
    """ Accepts a narrowed config, tapered just to the permission bits for this user.
    Sorts traversals into those that go to the many side of a relation,
    and those that go to the one side of a relation.
    """
    if from_res == 'index':
        local_fields = []
    else:
        local_fields = local_fields_of(model_for(from_res))
    result = {'one': [], 'many': {}}
    for k, v in config[from_res]['fields'].items():
        if v & 1:
            if k in local_fields:
                result['one'].append(k)
            else:
                methods = []
                if v & 4:
                    methods.append('GET')
                if v & 2:
                    methods.append('POST')
                result['many'][k] = methods
    return result


@MemoizeMutable
def instance_permissions(user, instance):
    """ How should this user see this instance? Figure's out the user's status
    compared to the instance, then figures owner/group/world for the user,
    then fires off a new copy of that permissions dictionary for that role.
    """
    top_group = user.status_over(instance.group)
    new_config = base_config(top_group.name)
    return reduce_permissions_dictionary_to(role_for(user, instance), new_config)
