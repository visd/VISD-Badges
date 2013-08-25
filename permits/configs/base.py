BASE_PERMISSIONS = {
    'index': {
        'fields': {
            'skillsets': '0755',
            'challenges': '0711',
            'entries': '0711',
            'tags': '0711',
            'tools': '0755'
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
            # 'owner': '0640',
            # 'group': '0600',
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
            'challenge': '0600'
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
            'title': '0744',
            'caption': '0744',
            'image': '0744',
            'url_link': '0744',
            'url_title': '0744',
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
            'word': '0744',
            'slug': '0000',
            'created_at': '000',
            'challenges': '0755',
            'resources': '0755',
            'skillsets': '0755'
        },
        'methods': {
            'PUT': '0700',
            'GET': '0555',
            'DELETE': '0500'
        }
    },
    'users': {
        'fields':
            {'first_name':'0640',
             'last_name':'0640',
             'email':'0640',
             'username':'0440',
             'groups':'0750'
            },
        'methods':
            {'PUT': '0700',
             'GET': '0550',
             'DELETE': '0500'}
        }
}