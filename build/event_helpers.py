"""
Use these to create phony events of the types defined in events.event_types.

The create_all_event_types function gets n of each, matches each one with a model and a phony user,
randomizes the date for each, then saves them in a batch.
"""

from random import randint
from datetime import datetime, timedelta
from importlib import import_module

from django.contrib.auth.models import User

from events.event_types import EVENT_TYPES
from build.resource_configs import RESOURCE_CONFIGS

from events.processors import register_event


def fetch_event_types():
    """ Returns a list of events in the EVENT_TYPES dictionary.

    Appends a config dictionary to each so we can know what resource this event-type is asking for.
    """
    event_types = []
    for key in EVENT_TYPES.iterkeys():
        event_types.append(key)
    return event_types


def fetch_config_dictionary(given_event_type):
    """Will return the dictionary on this particular resource from event_types
    """
    object = EVENT_TYPES[given_event_type]['object']
    try:
        return RESOURCE_CONFIGS[object]
    except KeyError:
        return 'No resource config found for %s' % object


def get_model_for_event(event_dict, create=False):
    """ Returns a model instance, either by making one from a factory or fetching a random one.

    Expects the dictionary returned by fetch_event_types.
    """
    if create:
        factory = event_dict['factory']
        from build import factories
        try:
            this_factory = getattr(factories, factory)
            model_instance = this_factory.__call__()
        except AttributeError:
            return "There is no factory for %s" % event_dict['model']
    else:
        which_module = '.'.join([event_dict['app'], 'models'])
        try:
            this_module = import_module(which_module)
            this_model = event_dict['model']
            try:
                model = getattr(this_module, this_model)
                # Warning! Very slow method alert. Write a more efficient method if you want.
                model_instance = model.objects.order_by('?')[0]
            except AttributeError:
                return '%s has no model named %s' % (this_module, this_model)
        except ImportError:
            return "There is no module named %s" % which_module
    return model_instance


def create_event(event_type):
    """ Takes one event_type, gets a model to fill it with, gets a user, then returns an event.
    
    Accepts a tuple of event_type, then a dictionary of key information (see resource_configs)
    """
    # fetch the config for this event
    event_config = fetch_config_dictionary(event_type)
    model_instance = get_model_for_event(event_config)
    # Again, a very slow method and only suitable for this testing environment.
    user = User.objects.order_by('?')[0]

    return register_event(model_instance, event_type, given_user=user)


def create_all_event_types(count=3):
    """ Pass in a count to create that many of each event type.
    """
    log = ''
    event_list = fetch_event_types()
    created_events = []
    for _ in range(count):
        for e in event_list:
            new_event = create_event(e)
            new_event = randomize_dates(new_event)
            created_events.append(new_event)
            log += str(new_event) + "\n"
    return [created_events, log]


def randomize_dates(event):
    """Accepts an event and pushes its date backwards by a random amount.
    """
    event.modified = event.modified - timedelta(hours=randint(0, 120))
    return event
