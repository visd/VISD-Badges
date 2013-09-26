BASE_PERMISSIONS = {
    'index': {
        'fields': {
            'skillsets': 'm755',
            'challenges': 'm711',
            'entries': 'm711',
            'tags': 'm711',
            'tools': 'm755',
            'events': 'm755',
            'users': 'm755',
            'groups': 'm500'
        },
        'methods': {
            'GET': '-444'
        }
    },
    'skillsets':{
        'fields':{
            'user': 'o500',
            'group': 'o700',
            'title': '-640',
            'short_description': '-640',
            'long_description': '-640',
            'slug': '-400',
            'created_at': '-000',
            'challenges': 'm755'
        },
        'methods': {
            'PUT': '-500',
            'GET': '-550',
            'DELETE': '-500'
        }
    },
    'challenges': {
        'fields': {
            'user': 'o550',
            'user_id': '-200',
            'group': 'o700',
            'group_id': '-200',
            'title': '-640',
            'short_description': '-640',
            'long_description': '-640',
            'slug': '-400',
            'created_at': '-000',
            'skillset': 'p550',
            'skillset_id': '-200',
            'entries': 'm755',
            'resources': 'm755',
            'tags': 'm755',
            'tools': 'm755'
        },
        'methods': {
            'PUT': '-700',
            'GET': '-550',
            'DELETE': '-500'
        }
    },
    'resources': {
        'fields': {
            'user': 'o600',
            'group': 'o600',
            'title': '-644',
            'url_link': '-644',
            'url_title': '-644',
            'description': '-644',
            'challenge': 'p644',
            'thumb': '-644',
            'created_at': '-400',
        },
        'methods': {
            'PUT': '-700',
            'GET': '-555',
            'DELETE': '-500'
        }
    },
    'entries': {
        'fields': {
            'user': 'o550',
            'group': 'o600',
            'title': '-644',
            'caption': '-644',
            'image': '-644',
            'url_link': '-644',
            'url_title': '-644',
            'created_at': '-444',
            'challenge': 'p550'
        },
        'methods': {
            'PUT': '-700',
            'GET': '-555',
            'DELETE': '-500'
        }
    },
    'tags': {
        'fields': {
            'user': 'o000',
            'group': 'o000',
            'word': '-644',
            'slug': '-000',
            'created_at': '-000',
            'challenges': 'm555',
            'entries': 'm555',
            'skillsets': 'm555'
        },
        'methods': {
            'PUT': '-700',
            'GET': '-550',
            'DELETE': '-500'
        }
    },
    'tools': {
        'fields': {
            'user': 'o000',
            'group': 'o000',
            'title': '-644',
            'slug': '-000',
            'url_link': '-644',
            'url_title': '-644',
            'icon': '-644',
            'created_at': '-000',
            'challenges': 'm555',
            'entries': 'm555'
        },
        'methods': {
            'PUT': '-700',
            'GET': '-555',
            'DELETE': '-500'
        }
    },
    'events': {
        'fields': {
            'created': '-400',
            'modified': '-400',
            'user': '-440',
            'tags': '-555'
        }
    },
    'users': {
        'fields': {
            'user': 'o000',
            'group': 'o000',
            'first_name': '-640',
            'last_name': '-640',
            'email': '-640',
            'memberships': 'm550',
            'entries': 'm555'
        },
        'methods': {
            'PUT': '-700',
            'GET': '-550',
            'DELETE': '-500'
        }
    },
    'memberships': {
        'fields': {
            'name': '-600',
            'parent': 'o000'
        },
        'methods': {
            'PUT': '-000',
            'GET': '-500',
            'DELETE': '-000'
        }
    }
}