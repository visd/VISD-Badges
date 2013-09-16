import random

from django.template.defaultfilters import slugify

import factory

from fuzzers import FishFuzz, HexFuzz, SlugFuzz, FirstNameFuzz, LastNameFuzz,\
RandomExistingUser, RandomExistingGroup

from badges.models import Skillset, Challenge, Tag, Tool, Resource, Entry
from custom_auth.models import CustomUser, NestedGroup
from events.models import Event

from . import event_helpers


def add_randomly_to_targets(target_model, target_field, list_to_add):
    """ This accepts a target model, its many-to-many field, and a list of instances to add
    via the many-to-many field.

    It walks through all the objects of the target model, then adds a random collection of objects to add.
    """
    targets = target_model.objects.all()

    results = []
    log = ''

    for target in targets:
        add_these = random.sample(
            list_to_add, random.randint(1, len(list_to_add)))
        field = getattr(target, target_field)
        field.add(*add_these)
        results.append(target)
        log += '%s, added %s\n' % (str(target), str(add_these))

    return [results, log]


class TagFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = Tag

    user = RandomExistingUser()
    group = factory.LazyAttribute(lambda t: t.user.groups.all()[0])
    word = SlugFuzz()


class GroupFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = NestedGroup
    
    name = factory.Iterator(['guest','visd-guest','visd-user','visd-staff','admin','fsd-guest','fsd-staff'])


class UserFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = CustomUser
    FACTORY_HIDDEN_ARGS = ('group_to_add',)
    group_to_add = 'visd-user'

    first_name = FirstNameFuzz()
    last_name = LastNameFuzz()
    email = factory.LazyAttribute(
        lambda t: ('%s_%s@vashonsd.org' % (t.first_name, t.last_name)).lower())
    password = HexFuzz()

    @factory.post_generation
    def add_groups(self, create, extracted, **kwargs):
        self.groups.add(RandomExistingGroup().fuzz())


class ToolFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = Tool

    user = RandomExistingUser()
    group = factory.LazyAttribute(lambda t: t.user.groups.all()[0])
    title = SlugFuzz()
    url_link = "http://www.example.com"
    url_title = factory.LazyAttribute(
        lambda t: "%s consectetur adipisicing elit. Temporibus eveniet enim et." % t.title)
    slug = factory.LazyAttribute(lambda t: slugify(t.title))


class SkillsetFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = Skillset

    user = RandomExistingUser()
    group = factory.LazyAttribute(lambda t: t.user.groups.all()[0])
    title = FishFuzz(1, 3)
    short_description = factory.LazyAttribute(
        lambda t: "%s gets to have a short description." % t.title)
    long_description = factory.LazyAttribute(
        lambda t: "%s gets a longer description of elit. Reprehenderit, iure optio saepe qui molestiae!" % t.title)
    id = factory.Sequence(lambda n: '1%d' % n)


class ChallengeFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = Challenge

    user = RandomExistingUser()
    group = factory.LazyAttribute(lambda t: t.user.groups.all()[0])
    skillset = factory.SubFactory(SkillsetFactory)
    title = factory.LazyAttributeSequence(
        lambda t, n: "Challenge #%d for %s" % (n, t.skillset))
    slug = factory.LazyAttribute(lambda t: slugify(t.title))
    short_description = factory.LazyAttribute(
        lambda t: "%s gets a short description." % t.title)
    long_description = factory.LazyAttribute(
        lambda t: "%s consectetur Lorem ipsum dolor sit amet, consectetur adipisicing elit." % t.title)


class ResourceFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = Resource

    user = RandomExistingUser()
    group = factory.LazyAttribute(lambda t: t.user.groups.all()[0])
    challenge = factory.SubFactory(ChallengeFactory)
    title = factory.LazyAttributeSequence(
        lambda t, n: 'Resource #%03d for %s' % (n, t.challenge))
    url_link = "http://www.example.com"
    url_title = "Lorem ipsum dolor sit amet."
    description = "Lorem ipsum dolor sit amet, consectetur adipisicing elit. Id itaque porro consequatur placeat adipisci?"
    thumb = "example.jpg"


class EntryFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = Entry

    user = RandomExistingUser()
    group = factory.LazyAttribute(lambda t: t.user.groups.all()[0])
    title = factory.LazyAttributeSequence(
        lambda t, n: "Entry #%d for %s" % (n, t.challenge))
    caption = "Students used two weeks of filming time to create this sped-up view of a plant's growth."
    # image = factory.django.ImageField(filename="example")
    url_link = "http://www.example.com"
    url_title = "How This Was Done"
    challenge = factory.SubFactory(ChallengeFactory)


def AllTypesOfEvents(count):
    return (event_helpers.create_all_event_types(count=1))


def add_groups_to_users():
    """ Pulls a random group, finds its children, then goes through the users, assigning them groups.
    """
    users = CustomUser.objects.all()
    results = []
    log = []
    for user in users:
        group = NestedGroup.objects.order_by('?')[0]
        user.groups.add(group)
        results.append(user)
        log.append('%s, added %s' % (str(user), str(group)))
    return [results, '\n'.join(log)]


def assign_parents_to_groups(count):
    group_list = [
        ('guest', 'visd-guest'), ('visd-guest', 'visd-user'), ('visd-user', 'visd-staff'),
        ('visd-staff', 'admin'), ('admin', ''), ('fsd-guest','fsd-staff'),('fsd-staff','')
    ]
    results = []
    log = []
    for g, p in group_list[:count]:
        if p:
            this_group = NestedGroup.objects.get_or_create(name=g)[0]
            this_parent = NestedGroup.objects.get_or_create(name=p)[0]
            this_group.parent = this_parent
            results.append(this_group)
            log.append('Group %s got a parent group %s' % (g, p))
    return [results, '\n'.join(log)]


def these_globals():
    return globals()


def ManyToManyFactory(count=2, create=None, join_to=None, target_field=None):
    """ This makes [count] of the factory given in [create],
    then joins a random number of each one to the list of models in join_to.
    """
    result = []
    joiners = []
    log = []
    factory = globals()[create]
    for _ in range(count):
        made = factory()
        joiners.append(made)
        result.append(made)
        log.append(str(made))
    for joinee in join_to:
        added = (add_randomly_to_targets(
                 globals()[joinee],
                 target_field,
                 joiners)
                 )
        log.append(added[1])
        result.extend(added[0])
    return [result, '\n'.join(log)]
