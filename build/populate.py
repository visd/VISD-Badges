from os import path

import yaml

import factory

from . import factories

from badges.models import Skillset, Challenge, Entry, Resource, Tool, Tag
from events.models import Event
from django.contrib.auth.models import User

"""
This module assumes you have created factories for models in your Django project, and that you have created
a YAML manifest showing the relations you want the factories to generate.

The outcome is to specify "Create 3 of resource A, each with 4 related resoure B" and so on throughout the 
tree of relations you specify.

Still to do:

- Split config data out of manifests to adhere to DRY principles. That is, have a separate config.yaml which
  matches resources to factories so manifests showing relations can be less verbose.

- Decouple from factory_boy. User should be able to register resources to any function that produces a dummy
  resource.
"""


def walk_factories(n, parent=None, result_list=[], result_log=[''], indent=0):
    """This walks recursively through the given tree, calling on factories and telling subnodes to call on factories.

    Relationships should be in the form of an acyclic directed graph.
    """
    for c in range(n['count']):
        # Find out if there's a parent on the stack. Pass it or None to make an instance of current node.
        inst = make_factory(n['factory'],
                            parent_field=n.get('parent_field'),
                            parent=parent)
        result_list.append(inst)
        result_log[0] += " " * indent + str(inst) + "\n"

        if n.get('children'):
            for child in n['children']:
                walk_factories(child,
                               parent=inst,
                               result_list=result_list,
                               result_log=result_log,
                               indent=indent + 4
                               )
    return [result_list, result_log[0]]


def make_factory(factory_class, parent_field=None, parent=None):
    """
    """
    c = getattr(factories, factory_class)
    
    if parent_field is not None:
        return factory.build(c, **{parent_field: parent})
    else:
        return factory.build(c)


def clear_data(mod_list=[Tool, Challenge, Skillset, Entry, Tag, Resource, Event, User]):
    """ Used to delete all instances of models.
    """

    # Pass a different list to delete a subset.
    
    for mod in mod_list:
        mod.objects.all().delete()


def load_manifest():
    """ Loads manifest data from the YAML file.
    """
    f = open(path.join(path.dirname(path.realpath(__file__)), 'manifests.yaml'))
    f = yaml.load(f)
    return f


def install_fixtures(choice='small', reset=True, save=False, verbose=False):
    """
    This is the dispatcher for loading the manifest, creating new fixtures and dependents,
    and creating new fixture to related to existing models.
    """
    
    manifests = load_manifest()['manifests']

    # Finds the manifests whose title matches the given choice.
    chosen_manifest = [m for m in manifests if m['title'] == choice][0]
   
    if reset:
        clear_data()
    
    # First, create the fixtures from scratch, including fixtures related to those.
    for node in chosen_manifest['premake']:
        result = (walk_factories(node))

    # At this point, result is a list of [[list of instances],'log']

    # # The 'postadd' phase is for calling factories that have to do more customized actions.
    # # Look to the individual factories to see what they do.
    # However: Every function must return a tuple of ([instances], 'log')

    for node in chosen_manifest['postadd']:
        which_func = node.pop('factory')
        # find the factory function specified in the manifest.
        f = getattr(factories, which_func)
        # now add the results of calling that function with the rest of the node as arguments.
        this_return = f.__call__(**node)
        result[0].extend(this_return[0])
        result[1] += this_return[1]

    if save:
        for inst in result[0]:
            inst.save()
        print "Instances saved."
    else:
        print "Instances not saved."
    
    return result


def list_manifests():
    t = load_manifest()
    return t['manifests']
