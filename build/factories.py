import random

from django.template.defaultfilters import slugify

import factory

from fuzzers import FishFuzz, HexFuzz, SlugFuzz, FirstNameFuzz, LastNameFuzz

from badges import models
from django.contrib.auth.models import User, Group
from events.models import Event
from events.event_types import EVENT_TYPES

class TagFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = models.Tag

    word = SlugFuzz()


class UserFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = User

    first_name = FirstNameFuzz()
    last_name = LastNameFuzz()
    username = factory.LazyAttribute(lambda t: ('%s%s' % (t.first_name[:1], t.last_name)).lower())
    password = HexFuzz()
    email = factory.LazyAttribute(lambda t: '%s@vashonsd.org' % t.username)
    

class ToolFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = models.Tool
    
    title = SlugFuzz()
    url_link = "http://www.example.com"
    url_title = factory.LazyAttribute(lambda t: "%s consectetur adipisicing elit. Temporibus eveniet enim et." % t.title)
    slug = factory.LazyAttribute(lambda t: slugify(t.title))


class SkillsetFactory(factory.Factory):
    FACTORY_FOR = models.Skillset
    
    title = FishFuzz(1,3)
    short_description = factory.LazyAttribute(lambda t: "%s gets to have a short description." % t.title)
    long_description = factory.LazyAttribute(lambda t: "%s gets a longer description of elit. Reprehenderit, iure optio saepe qui molestiae!" % t.title)
    id = factory.Sequence(lambda n: '1%d' % n)


class ChallengeFactory(factory.django.DjangoModelFactory):        
    FACTORY_FOR = models.Challenge

    skill = factory.SubFactory(SkillsetFactory)
    title = factory.LazyAttributeSequence(lambda t, n: "Challenge #%d for %s" % (n, t.skill))
    slug = factory.LazyAttribute(lambda t: slugify(t.title))
    short_description = factory.LazyAttribute(lambda t: "%s gets a short description." % t.title)
    long_description = factory.LazyAttribute(lambda t: "%s consectetur Lorem ipsum dolor sit amet, consectetur adipisicing elit." % t.title) 


class ResourceFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = models.Resource

    challenges = factory.SubFactory(ChallengeFactory)
    title = factory.LazyAttributeSequence(lambda t, n: 'Resource #%03d for %s' % (n, t.challenges))
    url_link = "http://www.example.com"
    url_title = "Lorem ipsum dolor sit amet."
    description = "Lorem ipsum dolor sit amet, consectetur adipisicing elit. Id itaque porro consequatur placeat adipisci?"
    thumb = "example.jpg"

    
class EntryFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = models.Entry

    user = factory.SubFactory(UserFactory)
    title = factory.LazyAttributeSequence(lambda t, n: "Entry #%d for %s" % (n, t.challenge))
    caption = "Students used two weeks of filming time to create this sped-up view of a plant's growth."
    # image = factory.django.ImageField(filename="example")
    url_link = "http://www.example.com"
    url_title = "How This Was Done"
    challenge = factory.SubFactory(ChallengeFactory)

class EventFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = Event


def fetch_event_types():
    for (key, item) in EVENT_TYPES.items():
        event_type = key
        resource = item['object']
        print "Event Type: %s, Resource: %s" % (event_type, resource)
