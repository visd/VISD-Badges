from django.db import models

# from django.core.urlresolvers import reverse

# class ListingQuerySet(models.query.QuerySet):
#     """ Helps us return the listing from a given model. This is the "shell" view; the bare essentials.
#     Eventually the definition of the fields in bare eseentials will come from a config file
#     so it is easily changeable.
#     """
#     def related(self, relation=None):
#         return self.filter(**relation)

# class ListingManager(models.Manager):
#     def get_query_set(self):
#         return ListingQuerySet(self.model, using = self._db)

#     def related(self, relation):
#         return self.get_query_set().related(relation)

class CollectionManager(models.Manager):
    """ Figures out the url for the collection of the manager's class.

    Allows us to call [class].objects.url(parent).

    Examples:

    >>> print Challenge.collection.url(parent='skillsets/43')
    'skillsets/43/challenges'

    >>> print Challenge.collection.url()
    'challenges'
    """

    use_for_related_fields = True

    def url(self, scoped=True):
        parent = self.__dict__.get('instance')
        return '%s/%s' % (scoped and (parent and ('%s' % parent.url)) or "", self.model._meta.verbose_name_plural)
