from django.contrib.auth.models import User, Group
from django.template.defaultfilters import slugify
from django.db import models
from django.core.urlresolvers import reverse

from .custom_managers import CollectionManager
from model_mixins import URLmixin
# from auth.models import UserProfile

import django.db.models.options as options

options.DEFAULT_NAMES = options.DEFAULT_NAMES + ('schema',)

# Note from AJ: to make the syncdb command work I had to comment out UserProfile -- 
# I believe it's deprecated in 1.5?

# class Index(models.Model):
#     sitename = models.CharField(max_length=32)
#     tagline = models.CharField(max_length=255)
#     site_owner = models.ForeignKey(User, related_name='sites')
#     site_group = models.ForeignKey(User, related_name='sites')


class Tag(URLmixin, models.Model):
    # owner = models.ForeignKey(User, related_name='tags')
    word = models.CharField(max_length=35)
    slug = models.SlugField()
    created_at = models.DateTimeField(auto_now_add=True)
    # challenges = models.ForeignKey('Challenge', related_name='Challenges')

    collection = CollectionManager()
    objects = models.Manager()

    def __unicode__(self):
        return "Tag: %s" % self.word

    def save(self, *args, **kwargs):
        self.slug = slugify(self.word)
        super(Tag, self).save(*args, **kwargs)

    class Meta:
        verbose_name=u'tag'
        verbose_name_plural=u'tags'


class Tool(URLmixin, models.Model):
    title = models.CharField(db_index=True, max_length=30, unique=True)
    slug = models.SlugField()
    url_link = models.URLField(max_length=300)
    url_title = models.CharField(max_length=140)
    icon = models.CharField(max_length=2) # Icon Font used?
    created_at = models.DateTimeField(auto_now_add=True)
    # challenges = models.ForeignKey('Challenge', related_name='Challenges')

    collection = CollectionManager()
    objects = models.Manager()

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Tool, self).save(*args, **kwargs)

    class Meta:
        verbose_name=u'tool'
        verbose_name_plural=u'tools'


class Entry(URLmixin, models.Model):
    id = models.AutoField(db_index=True, primary_key=True)
    user = models.ForeignKey(User)
    title = models.CharField(max_length=30)
    caption = models.CharField(max_length=140)
    image = models.ImageField(upload_to='photos/%Y/%m/%d/')
    url_link = models.URLField(max_length=300)
    url_title = models.CharField(max_length=140)
    created_at  = models.DateTimeField(auto_now_add=True)
    challenge = models.ForeignKey('Challenge', related_name='entries')

    collection = CollectionManager()
    objects = models.Manager()

    def __unicode__(self):
        # return "%(id)s, %(user)s: %(title)s" % locals()
        return "%s" % self.title   

    class Meta:
        verbose_name=u'entry'
        verbose_name_plural=u'entries'     
        

class Challenge(URLmixin, models.Model):
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

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Challenge, self).save(*args, **kwargs)

    class Meta:
        verbose_name = u'challenge'
        verbose_name_plural = u'challenges'


class Resource(URLmixin, models.Model):
    id = models.AutoField(db_index=True, primary_key=True)
    title = models.CharField(max_length=30)
    url_link = models.URLField(max_length=300)
    url_title = models.CharField(max_length=140)
    description = models.CharField(max_length=140)
    thumb = models.URLField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    challenge = models.ForeignKey(Challenge, related_name='resources')

    collection = CollectionManager()
    objects = models.Manager()

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = u'resource'
        verbose_name_plural = u'resources'


class Skillset(URLmixin, models.Model):
    title = models.CharField(db_index=True, max_length=30, unique=True)
    slug = models.SlugField()
    short_description = models.CharField(max_length=140)
    long_description = models.CharField(max_length=600)
    created_at = models.DateTimeField(auto_now_add=True)

    collection = CollectionManager()
    objects = models.Manager()

    def __unicode__(self):
        return 'Skillset %s' % self.title

    class Meta:
        verbose_name = u'skillset'
        verbose_name_plural = u'skillsets'
        schema = 'turkey'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Skillset, self).save(*args, **kwargs)
