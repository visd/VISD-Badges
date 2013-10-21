from custom_auth.models import NestedGroup
from django.template.defaultfilters import slugify
from django.db import models
# from django.core.urlresolvers import reverse

from django.conf import settings

from .custom_managers import CollectionManager
from model_mixins import URLmixin
from custom.utils import memoized_property
# from auth.models import CustomUser

import django.db.models.options as options

options.DEFAULT_NAMES = options.DEFAULT_NAMES + ('schema',)


class Tag(URLmixin, models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='tags')
    group = models.ForeignKey(NestedGroup, related_name='tags')
    word = models.CharField(max_length=35)
    slug = models.SlugField()
    created_at = models.DateTimeField(auto_now_add=True)
    # challenges = models.ForeignKey('Challenge', related_name='Challenges')

    collection = CollectionManager()
    objects = models.Manager()

    @memoized_property
    def parent_instance(self):
        return None

    def __unicode__(self):
        return "Tag: %s" % self.word

    def save(self, *args, **kwargs):
        self.slug = slugify(self.word)
        super(Tag, self).save(*args, **kwargs)

    class Meta:
        verbose_name = u'tag'
        verbose_name_plural = u'tags'


class Tool(URLmixin, models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='tools')
    group = models.ForeignKey(NestedGroup, related_name='tools')
    title = models.CharField(db_index=True, max_length=256, unique=True)
    slug = models.SlugField()
    url_link = models.URLField(max_length=300)
    url_title = models.CharField(max_length=140)
    icon = models.CharField(max_length=2)  # Icon Font used?
    created_at = models.DateTimeField(auto_now_add=True)
    # challenges = models.ForeignKey('Challenge', related_name='Challenges')

    collection = CollectionManager()
    objects = models.Manager()

    @memoized_property
    def parent_instance(self):
        return None

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Tool, self).save(*args, **kwargs)

    class Meta:
        verbose_name = u'tool'
        verbose_name_plural = u'tools'


class Entry(URLmixin, models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='entries')
    group = models.ForeignKey(NestedGroup, related_name='entries')
    title = models.CharField(max_length=256)
    caption = models.CharField(max_length=140)
    image = models.ImageField(upload_to='photos/%Y/%m/%d/')
    url_link = models.URLField(max_length=300)
    url_title = models.CharField(max_length=140)
    created_at = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag, related_name='entries')
    tools = models.ManyToManyField(Tool, related_name='entries')
    challenge = models.ForeignKey('Challenge', related_name='entries')

    @memoized_property
    def parent_instance(self):
        return self.challenge

    collection = CollectionManager()
    objects = models.Manager()

    def __unicode__(self):
        # return "%(id)s, %(user)s: %(title)s" % locals()
        return "%s" % self.title

    class Meta:
        verbose_name = u'entry'
        verbose_name_plural = u'entries'


class Challenge(URLmixin, models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='challenges')
    group = models.ForeignKey(NestedGroup, related_name='challenges')

    title = models.CharField(db_index=True, max_length=256, unique=True)
    slug = models.SlugField()
    skillset = models.ForeignKey('Skillset', related_name='challenges')
    short_description = models.CharField(max_length=140)
    long_description = models.CharField(max_length=600)
    tags = models.ManyToManyField(Tag, related_name='challenges')
    tools = models.ManyToManyField(Tool, related_name='challenges')
    created_at = models.DateTimeField(auto_now_add=True)

    collection = CollectionManager()
    objects = models.Manager()

    @memoized_property
    def parent_instance(self):
        return self.skillset

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Challenge, self).save(*args, **kwargs)

    class Meta:
        verbose_name = u'challenge'
        verbose_name_plural = u'challenges'


class Resource(URLmixin, models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='resources')
    group = models.ForeignKey(NestedGroup, related_name='resources')

    title = models.CharField(max_length=256)
    url_link = models.URLField(max_length=300)
    url_title = models.CharField(max_length=140)
    description = models.CharField(max_length=140)
    thumb = models.URLField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    challenge = models.ForeignKey(Challenge, related_name='resources')

    collection = CollectionManager()
    objects = models.Manager()

    @memoized_property
    def parent_instance(self):
        return self.challenge

    @memoized_property
    def parent_instance_model(cls):
        return Challenge

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = u'resource'
        verbose_name_plural = u'resources'


class Skillset(URLmixin, models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='skillsets')
    group = models.ForeignKey(NestedGroup, related_name='skillsets')
    title = models.CharField(db_index=True, max_length=256, unique=True)
    slug = models.SlugField()
    short_description = models.CharField(max_length=140)
    long_description = models.CharField(max_length=600)
    created_at = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag, related_name='skillsets')

    collection = CollectionManager()
    objects = models.Manager()

    def __unicode__(self):
        return 'Skillset %s' % self.title

    @memoized_property
    def parent_instance(self):
        return None

    class Meta:
        verbose_name = u'skillset'
        verbose_name_plural = u'skillsets'
        schema = 'turkey'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Skillset, self).save(*args, **kwargs)
