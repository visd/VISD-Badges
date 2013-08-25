""" The depth number reflects how many steps down the recursive views we are.

To give an example:

/foos/78 - Depth 0.

if we automatically get

/foos/78/bars - Depth 1

and then:

/foos/78/bars/[:id] - Depth 2

We condition these because we really do not want to see everything of everything we are looking at.
The template system should just render what it's given and not try to make these kinds of decisions.

"""

VIEW_DEPTHS = {
    'skillsets': {

    },
    'challenges': {
        0: {},
        1: {
            'fields':
                {'omit':[
                    'long_description','slug','created_at','entries','resources','tools','skillset'
                    ]
                 'extend':[
                    'resources'
                    ]
                },
            'methods':
                {'omit':[
                    'PUT'
                    ]
                }
        },
        2: {
            'fields':
                {'omit':[
                    'long_description','short_description','slug','created_at','entries','resources','tags','tools','skillset'
                    ]
                },
            'methods': 
                {'omit':[
                    'PUT','DELETE'
                    ]
                }
        }
    }
}
