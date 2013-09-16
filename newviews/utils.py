import cPickle


class MemoizeMutable:
    def __init__(self, fn):
        self.fn = fn
        self.memo = {}

    def __call__(self, *args, **kwds):
        str = cPickle.dumps(args, 1)+cPickle.dumps(kwds, 1)
        if not str in self.memo:
            self.memo[str] = self.fn(*args, **kwds)

        return self.memo[str]


@MemoizeMutable
def _figure_role(inst_creds, user_id, user_memberships):
    """ For testing and dependency injection.
    Pass a tuple of (user_id,group_id)
    from the instance, and a list of groups from the user's memberships,
    then return 'owner', 'group' or 'world'.

    >>>print _figure_role((3, 'foo'), 3, ['foo', 'bar', 'baz'])
    'owner'

    >>>print _figure_role((3, 'foo'), 3, ['foo', 'bar', 'baz'])
    'group'

    >>>print _figure_role((3, 'wat'), 3, ['foo', 'bar', 'baz'])
    'world'

    """
    if inst_creds[0] == user_id:
        return 'owner'
    else:
        return inst_creds[1] in user_memberships and 'group' or 'world'


if __name__ == '__main__':
    import doctest
    doctest.testmod()
