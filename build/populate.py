import random
from os import path
import getopt

import yaml

import factory

from . import factories

from badges import models
from django.contrib.auth.models import User

from build import event_helpers

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
        result_list.append(inst)

        if n.get('children'):
            for child in n['children']:
                depthFirstTraverse(child, parent=inst)
    return result_list


def make_factory(factory_class, parent_field=None, parent=None):
    """
    """
    c = getattr(factories, factory_class)
    
    if parent_field is not None:
        return factory.build(c, **{parent_field: parent})
    else:
        return factory.build(c)


def clear_data(mod_list = ['Tool', 'Challenge', 'Skillset', 'Entry', 'Tag', 'Resource']):
    """ Used to delete all instances of models. 
    """

    # Pass a different list to delete a subset.
    
    for mod in mod_list:
        m = getattr(models, mod)
        m.objects.all().delete()
        User.objects.all().delete()


def load_manifest():
    """ Loads manifest data from the YAML file.
    """
    f = open(path.join(path.dirname(path.realpath(__file__)),'manifests.yaml'))
    f = yaml.load(f)
    return f


def install_fixtures(choice='small', reset=True, save=True):
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
        result = (depthFirstTraverse(node))

    # # The 'postadd' phase is for calling factories that have to do more customized actions.
    # # Look to the individual factories to see what they do.

    for node in chosen_manifest['postadd']:
        which_func = node.pop('factory')
        # find the factory function specified in the manifest.
        f = getattr(factories, which_func)
        # now add the results of calling that function with the rest of the node as arguments.
        print "calling %s with attributes %s" % (str(f),str(node))
        result.append(f.__call__(**node))
    
    return result
    # Go and make the number of events specified in this manifest


def list_manifests():
    t = load_manifest()
    return t['manifests']

if __name__ == '__main__':
    main()