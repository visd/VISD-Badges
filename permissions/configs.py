BASE_PERMISSIONS = {
    'index': {
        'skillsets': '0755',
        'challenges': '0755',
        'entries': '0755',
        'resources': '0755',
        'tags': '0755',
        'tools': '0755'
    },
    'skillset': {
        'fields':
            {'title': '0640',
            'short_description': '0640',
            'long_description': '0640',
            'owner': '0640',
            'group': '0600',
            'slug': '0400',
            'created_at': '0000',
            'challenge_set': '0555'},
        'methods':
            {'PUT': '0500',
             'GET': '0555',
             'DELETE': '0500',}
    },
}