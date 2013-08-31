BASE_PERMISSIONS = {
    'index': {
        'fields': {
            'skillsets': '0755',
            'challenges': '0711',
            'entries': '0711',
            'tags': '0711',
            'tools': '0755',
            'events': '0755'
        },
        'methods': {
            'GET': '0444'
        }
    },
    'skillsets': {
        'fields': {
            'title': '0640',
            'short_description': '0640',
            'long_description': '0640',
            # 'owner': '0640',
            # 'group': '0600',
            'slug': '0400',
            'created_at': '0000',
            'challenges': '0755'
        },
        'methods': {
            'PUT': '0500',
            'GET': '0555',
            'DELETE': '0500'
        }
    },
    'challenges': {
        'fields': {
            'title': '0640',
            'short_description': '0640',
            'long_description': '0640',
            'slug': '0400',
            'created_at': '0000',
            'skillset': '0600',
            'entries': '0755',
            'resources': '0755',
            'tags': '0755',
            'tools': '0755'
        },
        'methods': {
            'PUT': '0700',
            'GET': '0555',
            'DELETE': '0500'
        }
    },
    'resources': {
        'fields': {
            'title': '0644',
            'url-link': '0644',
            'url-title': '0644',
            'description': '0644',
            'challenge': '0644',
            'thumb': '0644',
            'created_at': '0400',
            'challenge': '0600',
            'entries': '0775'
        },
        'methods': {
            'PUT': '0700',
            'GET': '0555',
            'DELETE': '0500'
        }
    },
    'entries': {
        'fields': {
            'user': '0444',
            'title': '0644',
            'caption': '0644',
            'image': '0644',
            'url_link': '0644',
            'url_title': '0644',
            'created_at': '0444',
            'challenge': '0600'
        },
        'methods': {
            'PUT': '0700',
            'GET': '0555',
            'DELETE': '0500'
        }
    },
    'tags': {
        'fields':{
            'word': '0644',
            'slug': '0000',
            'created_at': '0000',
            'challenges': '0555',
            'resources': '0555',
            'skillsets': '0555'
        },
        'methods': {
            'PUT': '0700',
            'GET': '0555',
            'DELETE': '0500'
        }
    },
    'tools': {
        'fields':{
            'title': '0644',
            'slug': '0000',
            'url_link': '0644',
            'url_title': '0644',
            'icon': '0644',
            'created_at': '0000',
            'challenges': '0555',
            'resources': '0555',
            'skillsets': '0555',
            'entries': '0555'
        },
        'methods': {
            'PUT': '0700',
            'GET': '0555',
            'DELETE': '0500'
        }
    },
    'events': {
        'fields': {
            'created': '0400',
            'modified': '0400',
            'user': '0440',
            'tags': '0555'
        }
    # },
    # 'users': {
    #     'fields': {
    #         'first_name':'0640',
    #         'last_name':'0640',
    #         'email':'0640',
    #         'username':'0440',
    #         'groups':'0550',
    #         'entries': '0555'
    #     },
    #     'methods': {
    #         'PUT': '0700',
    #         'GET': '0550',
    #         'DELETE': '0500'
    #     }
    }
}