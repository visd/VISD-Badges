from helpers import memoized_property


class URLmixin(object):
    @memoized_property
    def url(self):
        return "/%s/%s" % (self._meta.verbose_name_plural, self.pk)
