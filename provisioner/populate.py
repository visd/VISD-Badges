import random
from os import path
import getopt

import yaml

import factory

from . import factories

from badges import models

result_list=[]

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

def depthFirstTraverse(n, parent=None):
    """This walks recursively through the given tree, calling on factories and telling subnodes to call on factories.

    Relationships should be in the form of an acyclic directed graph.
    """
    for c in range(n['count']):
        # Find out if there's a parent on the stack. Pass it or None to make an instance of current node.
        inst = make_factory(n['factory'], 
                            parent_field=n.get('parent_field'),
                            parent=parent)
        result_list.append('Created %s from %s' % (str(inst),n['factory']))

        if n.get('children'):
            for child in n['children']:
                depthFirstTraverse(child, parent=inst)
    return result_list


def make_factory(factory_class, parent_field=None, parent=None):
    """
    """
    c = getattr(factories, factory_class)
    
    if parent_field is not None:
        return factory.create(c, **{parent_field: parent})
    else:
        return factory.create(c)


def add_randomly_to_targets(target_model, target_field, list_to_add):
    """ This accepts a target model, its many-to-many field, and a list of instances to add
    via the many-to-many field.

    It walks through all the objects of the target model, then adds a random collection of objects to add.
    """
    m = getattr(models, target_model)
    targets = m.objects.all()

    result_log = []

    for target in targets:
        add_these = random.sample(list_to_add, random.randint(1,len(list_to_add)))
        field = getattr(target, target_field)
        field.add(*add_these)
        result_log.append((target,add_these))

    return result_log


def clear_data():
    for mod in ['Tool', 'Challenge', 'Skillset','Entry','Tag','Resource']:
        m = getattr(models, mod)
        m.objects.all().delete()


def load_manifest():
    f = open(path.join(path.dirname(path.realpath(__file__)),'manifests.yaml'))
    f = yaml.load(f)
    # f = Struct(f)
    return f


def install_fixtures(choice='small', reset=True):
    """
    This is the dispatcher for loading the manifest, creating new fixtures and dependents,
    and creating new fixture to related to existing models.
    """    
    result = []
    manifests = load_manifest()['manifests']

    chosen_manifest = [m for m in manifests if m['title'] == choice][0]
   
    if reset:
        clear_data()
    
    # First, create the fixtures from scratch, including fixtures related to those.
    for node in chosen_manifest['premake']:
        result.append(depthFirstTraverse(node))

    # Now that we have fixtures we can create the many-to-many relationships.
    for node in chosen_manifest['postadd']:
        # First, get a list of factory-made foos:
        to_add = []
        for c in range(node['count']):
            to_add.append(make_factory(node['factory']))
        # Then add a random numbers of foos to the targetmodel:
        result.append(add_randomly_to_targets(node['targetmodel'], node['targetfield'], to_add))
    return result


def list_manifests():
    t = load_manifest()
    return t['manifests']

if __name__ == '__main__':
    main()