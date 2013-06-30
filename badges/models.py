from django.contrib.auth.models import User, Group
from django.db import models

class Badge(models.Model):
    title = models.CharField(max_length=30)

class Tag(models.Model):
    word        = models.CharField(db_index=True, max_length=35, unique=True)
    slug        = models.CharField(max_length=250)
    created_at  = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.word

    class Meta:
        ordering = ['word']

class Challenges(models.Model):
    title = models.CharField(db_index=True, max_length=30, unique=True)
    # skill = models.ForeignKey('Skillset', verbose_name=u'skill that challenge bellongs to')
    short_description = models.CharField(max_length=140)
    long_description = models.CharField(max_length=600)
    tags = models.ManyToManyField(Tag)

    class Meta:
        ordering = ['title']

class Skillset(models.Model):
    title = models.CharField(db_index=True, max_length=30, unique=True)
    short_description = models.CharField(max_length=140)
    long_description = models.CharField(max_length=600)
    challenges_list = models.ManyToManyField(Challenges, verbose_name=u'list of challenges')

    class Meta:
        ordering = ['title']


class Entries(models.Model):
    id = models.AutoField(db_index=True, primary_key=True)
    user = models.OneToOneField(User, verbose_name=u'creator of entry')
    title = models.CharField(max_length=30)
    caption = models.CharField(max_length=140)
    image = models.URLField(max_length=300)
    url_link = models.URLField(max_length=300)
    url_title = models.CharField(max_length=140)
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['user']


class Resource(models.Model):
    id = models.AutoField(db_index=True, primary_key=True)
    title = models.CharField(max_length=30)
    url_link = models.URLField(max_length=300)
    url_title = models.CharField(max_length=140)
    description = models.CharField(max_length=140)
    thumb = models.URLField(max_length=300)

class Tool(models.Model):
    title = models.CharField(db_index=True, max_length=30, unique=True)
    url_link = models.URLField(max_length=300)
    url_title = models.CharField(max_length=140)
    icon = models.CharField(max_length=2) # Icon Font used?

    class Meta:
        ordering = ['title']

