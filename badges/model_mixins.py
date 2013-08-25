class memoized_property(object):
    """A read-only @property that is only evaluated once.
    See http://www.reddit.com/r/Python/comments/ejp25/cached_property_decorator_that_is_memory_friendly/
    """
    def __init__(self, fget, doc=None):
        self.fget = fget
        self.__doc__ = doc or fget.__doc__
        self.__name__ = fget.__name__

    def __get__(self, obj, cls):
        if obj is None:
            return self
        obj.__dict__[self.__name__] = result = self.fget(obj)
        return result

class URLmixin(object):
    @memoized_property
    def url(self):
        return "/%s/%s" % (self._meta.verbose_name_plural, self.pk)