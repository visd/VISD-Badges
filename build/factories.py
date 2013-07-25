import random

from django.template.defaultfilters import slugify

import factory

from fuzzers import FishFuzz, HexFuzz, SlugFuzz, FirstNameFuzz, LastNameFuzz

from badges.models import Skillset, Challenge, Tag, Tool, Resource, Entry
from django.contrib.auth.models import User, Group
from events.models import Event

from . import event_helpers


def add_randomly_to_targets(target_model, target_field, list_to_add):
    """ This accepts a target model, its many-to-many field, and a list of instances to add
    via the many-to-many field.

    It walks through all the objects of the target model, then adds a random collection of objects to add.
    """
    targets = target_model.objects.all()

    results = []
    log =''

    for target in targets:
        add_these = random.sample(list_to_add, random.randint(1,len(list_to_add)))
        field = getattr(target, target_field)
        field.add(*add_these)
        results.append(target)
        log += '%s, added %s\n' % (str(target),str(add_these))

    return [results, log]


class TagFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = Tag

    word = SlugFuzz()


class UserFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = User

    first_name = FirstNameFuzz()
    last_name = LastNameFuzz()
    username = factory.LazyAttribute(lambda t: ('%s_%s' % (t.first_name, t.last_name)).lower())
    password = HexFuzz()
    email = factory.LazyAttribute(lambda t: '%s@vashonsd.org' % t.username)


class ToolFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = Tool
    
    title = SlugFuzz()
    url_link = "http://www.example.com"
    url_title = factory.LazyAttribute(lambda t: "%s consectetur adipisicing elit. Temporibus eveniet enim et." % t.title)
    slug = factory.LazyAttribute(lambda t: slugify(t.title))


class SkillsetFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = Skillset
    
    title = FishFuzz(1,3)
    short_description = factory.LazyAttribute(lambda t: "%s gets to have a short description." % t.title)
    long_description = factory.LazyAttribute(lambda t: "%s gets a longer description of elit. Reprehenderit, iure optio saepe qui molestiae!" % t.title)
    id = factory.Sequence(lambda n: '1%d' % n)


class ChallengeFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = Challenge

    skill = factory.SubFactory(SkillsetFactory)
    title = factory.LazyAttributeSequence(lambda t, n: "Challenge #%d for %s" % (n, t.skill))
    slug = factory.LazyAttribute(lambda t: slugify(t.title))
    short_description = factory.LazyAttribute(lambda t: "%s gets a short description." % t.title)
    long_description = factory.LazyAttribute(lambda t: "%s consectetur Lorem ipsum dolor sit amet, consectetur adipisicing elit." % t.title) 


class ResourceFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = Resource

    challenges = factory.SubFactory(ChallengeFactory)
    title = factory.LazyAttributeSequence(lambda t, n: 'Resource #%03d for %s' % (n, t.challenges))
    url_link = "http://www.example.com"
    url_title = "Lorem ipsum dolor sit amet."
    description = "Lorem ipsum dolor sit amet, consectetur adipisicing elit. Id itaque porro consequatur placeat adipisci?"
    thumb = "example.jpg"

    
class EntryFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = Entry

    user = factory.SubFactory(UserFactory)
    title = factory.LazyAttributeSequence(lambda t, n: "Entry #%d for %s" % (n, t.challenge))
    caption = "Students used two weeks of filming time to create this sped-up view of a plant's growth."
    # image = factory.django.ImageField(filename="example")
    url_link = "http://www.example.com"
    url_title = "How This Was Done"
    challenge = factory.SubFactory(ChallengeFactory)


def AllTypesOfEvents(count):
    return (event_helpers.create_all_event_types(count=1))


def these_globals():
    return globals()


def ManyToManyFactory(count=2, create=None, join_to=None, target_field=None):
    """ This makes [count] of the factory given in [create],
    then joins a random number of each one to the list of models in join_to.
    """
    result = []
    joiners = []
    log = ''
    factory = globals()[create]
    for _ in range(count):
        made = factory()
        joiners.append(made)
        result.append(made)
        log += str(made) + "\n"
    for joinee in join_to:
        added = (add_randomly_to_targets(
                      globals()[joinee],
                      target_field,
                      joiners)
                      )
        log += added[1]
        result.extend(added[0])
    return [result, log]