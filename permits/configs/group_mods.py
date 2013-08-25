MODS = {
    'visd-staff':{
        'skillsets': {
            'fields': {
                'title': '+w',
                'short_description': '+w',
                'long_description': '+w',
                'slug': '+rw',
                'challenges': '+w'
            },
            'methods':{
                'PUT': '+rwx',
                'DELETE': '+rx'
            }
        },
        'challenges': {
            'fields': {
                'title': '+w'
            },
            'methods': {
                'PUT': '+rwx'
            }
        }
    }
}