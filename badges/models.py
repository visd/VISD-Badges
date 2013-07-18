from django.contrib.auth.models import User, Group
from django.template.defaultfilters import slugify
from django.db import models


class Tag(models.Model):
    word = models.CharField(max_length=35)
    slug = models.SlugField()
    created_at = models.DateTimeField(auto_now_add=True)
    # challenges = models.ForeignKey('Challenge', related_name='Challenges')

    def __unicode__(self):
        return self.word

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
    challenge = models.ForeignKey('Challenge')

    def __unicode__(self):
        return "%(id)s, %(user)s: %(title)s" % locals()


class Challenge(models.Model):
    title = models.CharField(db_index=True, max_length=30, unique=True)
    slug = models.SlugField()
    skill = models.ForeignKey('Skillset')
    short_description = models.CharField(max_length=140)
    long_description = models.CharField(max_length=600)
    tags = models.ManyToManyField(Tag)
    resources = models.ManyToManyField('Resource')
    tools = models.ManyToManyField(Tool)
    # entries = models.ManyToManyField(Entry)
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
            self.slug = slugify(self.title)
            super(Challenge, self).save(*args, **kwargs)


class Resource(models.Model):
    id = models.AutoField(db_index=True, primary_key=True)
    title = models.CharField(max_length=30)
    url_link = models.URLField(max_length=300)
    url_title = models.CharField(max_length=140)
    description = models.CharField(max_length=140)
    thumb = models.URLField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    challenges = models.ForeignKey(Challenge)

    def __unicode__(self):
        return self.title


class Skillset(models.Model):
    title = models.CharField(db_index=True, max_length=30, unique=True)
    slug = models.SlugField()
    short_description = models.CharField(max_length=140)
    long_description = models.CharField(max_length=600)
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
            self.slug = slugify(self.title)
            super(Skillset, self).save(*args, **kwargs)

