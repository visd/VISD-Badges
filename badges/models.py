from django.contrib.auth.models import User, Group
from django.template.defaultfilters import slugify
from django.db import models
from django.core.urlresolvers import reverse

from .custom_managers import CollectionManager
# from auth.models import UserProfile

# Note from AJ: to make the syncdb command work I had to comment out UserProfile -- 
# I believe it's deprecated in 1.5?

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


class Tag(models.Model):
    word = models.CharField(max_length=35)
    slug = models.SlugField()
    created_at = models.DateTimeField(auto_now_add=True)
    # challenges = models.ForeignKey('Challenge', related_name='Challenges')

    def __unicode__(self):
        return "Tag: %s" % self.word

    def save(self, *args, **kwargs):
        self.slug = slugify(self.word)
        super(Tag, self).save(*args, **kwargs)


class Tool(models.Model):
    title = models.CharField(db_index=True, max_length=30, unique=True)
    slug = models.SlugField()
    url_link = models.URLField(max_length=300)
    url_title = models.CharField(max_length=140)
    icon = models.CharField(max_length=2) # Icon Font used?
    created_at = models.DateTimeField(auto_now_add=True)
    # challenges = models.ForeignKey('Challenge', related_name='Challenges')

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Tool, self).save(*args, **kwargs)


class Entry(models.Model):
    id = models.AutoField(db_index=True, primary_key=True)
    user = models.ForeignKey(User)
    title = models.CharField(max_length=30)
    caption = models.CharField(max_length=140)
    image = models.ImageField(upload_to='photos/%Y/%m/%d/')
    url_link = models.URLField(max_length=300)
    url_title = models.CharField(max_length=140)
    created_at  = models.DateTimeField(auto_now_add=True)
    challenge = models.ForeignKey('Challenge', related_name='entries')

    def __unicode__(self):
        # return "%(id)s, %(user)s: %(title)s" % locals()
        return "%s" % self.title        
        

class Challenge(models.Model):
    title = models.CharField(db_index=True, max_length=30, unique=True)
    slug = models.SlugField()
    skillset = models.ForeignKey('Skillset', related_name='challenges')
    short_description = models.CharField(max_length=140)
    long_description = models.CharField(max_length=600)
    tags = models.ManyToManyField(Tag)
    tools = models.ManyToManyField(Tool)
    created_at = models.DateTimeField(auto_now_add=True)
    
    collection = CollectionManager()
    objects = models.Manager()

    @memoized_property
    def url(self):
        return "/%s/%s" % (self._meta.verbose_name_plural, self.pk)

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Challenge, self).save(*args, **kwargs)

    class Meta:
        verbose_name = u'challenge'
        verbose_name_plural = u'challenges'


class Resource(models.Model):
    id = models.AutoField(db_index=True, primary_key=True)
    title = models.CharField(max_length=30)
    url_link = models.URLField(max_length=300)
    url_title = models.CharField(max_length=140)
    description = models.CharField(max_length=140)
    thumb = models.URLField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    challenge = models.ForeignKey(Challenge, related_name='resources')

    def __unicode__(self):
        return self.title


class Skillset(models.Model):
    title = models.CharField(db_index=True, max_length=30, unique=True)
    slug = models.SlugField()
    short_description = models.CharField(max_length=140)
    long_description = models.CharField(max_length=600)
    created_at = models.DateTimeField(auto_now_add=True)

    collection = CollectionManager()
    objects = models.Manager()

    @memoized_property
    def url(self):
        return "hey! you found my url!"

    def challenges(self):
        return self.challenge_set.objects.all()

    def __unicode__(self):
        return 'Skillset %s' % self.title

    class Meta:
        verbose_name = u'skillset'
        verbose_name_plural = u'skillsets'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Skillset, self).save(*args, **kwargs)

