""" The depth number reflects how many steps down the recursive views we are.

To give an example:

/foos/78 - Depth 0.

if we automatically get

/foos/78/bars - Depth 1

and then:

/foos/78/bars/[:id] - Depth 2

We condition these because we really do not want to see everything of everything we are looking at.
The template system should just render what it's given and not try to make these kinds of decisions.

Omissions are cumulative. The parser goes up the list from 0 up picking up fields to omit.

You can specify 'unomit' to put something back.
"""

from custom.utils import memoized

VIEW_DEPTHS = {
    'challenges': {
        0: {},
        1: {
            'fields': {
                'omit': [
                    'long_description', 'slug', 'created_at', 'entries', 'resources', 'tools'
                ],
                'extend': [
                    'resources'
                ]
            },
            'methods': {
                'omit': [
                    'PUT'
                ]
            }
        },
        2: {
            'fields': {
                'omit': [
                    'tags'
                ]
            },
            'methods': {
                'omit': [
                    'DELETE'
                ]
            }
        }
    },
    'skillsets': {
        0: {},
        1: {
            'fields': {
                'omit': [
                    'long_description', 'slug', 'created_at', 'tools'
                ],
                'extend': [
                    'resources'
                ]
            },
            'methods': {
                'omit': [
                    'PUT'
                ]
            }
        },
        2: {
            'fields': {
                'omit': [
                    'tags', 'short_description'
                ]
            },
            'methods': {
                'omit': [
                    'DELETE'
                ]
            }
        }
    },
    'entries': {
        0: {},
        1: {
            'fields': {
                'omit': [
                    'caption', 'tags', 'tools'
                ]
            }
        },
        2: {
            'fields': {
                'omit': [
                    'challenge', 'url_link', 'url_title', 'created_at'
                ]
            },
            'methods': {
                'omit': [
                    'PUT', 'DELETE'
                ]
            }
        }
    },
    'tools': {
        0: {},
        1: {
            'fields': {
                'omit': [
                    'challenges', 'entries', 'url_link', 'url_title', 'create_at'
                ]
            },
            'methods': {
                'omit': [
                    'PUT', 'DELETE'
                ]
            }
        },
        2: {
            'fields': {
                'omit': [
                    'icon', 'slug'
                ]
            },
        }
    },
    'resources': {
        0: {},
        1: {
            'fields': {
                'omit': [
                    'challenge', 'created_at'
                ]
            },
            'methods': {
                'omit': [
                    'PUT', 'DELETE'
                ]
            }
        }
    },
    'tags': {
        0: {},
        1: {
            'fields': {
                'omit': [
                    'user','group','created_at','challenges','entries','skillsets'
                ]
            }
        },
        2: {
            'methods': {
                'omit': [
                    'PUT', 'DELETE'
                ]
            }
        }
    }
}

def compile_mod_to(mod_fragment, depth):
    """Returns a dictionary with a set of fields to omit and a set of methods to omit. 
    """
    omit_dict = {'fields':set([]),'methods':set([])}
    for this_depth in [v for (k,v) in sorted(mod_fragment.items()) if k<=depth]:
        for key in this_depth:
            omit_dict[key] = (set(this_depth[key].get('omit',[])) | omit_dict[key]) - set(this_depth[key].get('unomit',[]))
    # Reconvert to lists.
    return {k:list(v) for (k,v) in omit_dict.items()}


def filter_permissions_for(resource, config, depth):
    """ given a resource name, a config for that resource and a target depth, use VIEW_DEPTHS
    to return a dictionary with fields and methods omitted.

    Think of the result as foreshortened.
    """
    mod = VIEW_DEPTHS.get(resource)
    if mod:
        compiled_mod = compile_mod_to(mod, depth)
        new_dict ={}
        for key, value in config.items():
            if compiled_mod.get(key):
                new_dict[key] = {k:v for (k,v) in config[key].items() if k not in compiled_mod[key]}
            else:
                new_dict[key] = value
        return new_dict
    else:
        return config
