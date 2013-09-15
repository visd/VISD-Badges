import collections
import functools
import cPickle
from importlib import import_module

from badges.resource_configs import config_from_verbose




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


class MemoizeMutable:
    def __init__(self, fn):
        self.fn = fn
        self.memo = {}

    def __call__(self, *args, **kwds):
        str = cPickle.dumps(args, 1)+cPickle.dumps(kwds, 1)
        if not str in self.memo: 
            self.memo[str] = self.fn(*args, **kwds)
        
        return self.memo[str]


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


@MemoizeMutable
def role_for(user, all_user_groups, instance):
    """ Looks up the instance's user/group and compares against the user
    and the user's list of all groups. Then determines if the user is the
    owner, group or world of this instance.
    """
    if user == getattr(instance, 'user', None):
        user_role = 'owner'
    elif hasattr(instance, 'group'):
        if instance.group.name in all_user_groups:
            user_role = 'group'
    else:
        user_role = 'world'
    return user_role


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
