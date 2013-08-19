BASE_RESOURCES = {
    'skillset': {
        'app': 'badges',
        'model': 'Skillset',
        'factory': 'SkillsetFactory',
        'permissions':
            {'class': '0755',
             'methods':
                {'GET': '0555',
                 'POST': '0500'},
             'each': 
                {'fields':
                    {'title': '0640',
                    'short_description': '0640',
                    'long_description': '0640',
                    'owner': '0640',
                    'group': '0600',
                    'slug': '0400',
                    'created_at': '0000'},
                'methods':
                    {'PUT': '0500',
                     'GET': '0555',
                     'DELETE': '0500',
                     'POST': '0500'}}
            },
        'children': ['challenge'],
        'many': ['tags','tools'],
        'parents':[]
    # },
    # 'challenge': {
    #     'app': 'badges',
    #     'model': 'Challenge',
    #     'factory': 'ChallengeFactory',
    #     'permissions':
    #         {'class': 0755,
    #         'fields':
    #             {'title': 0640,
    #             'short_description': 0640,
    #             'long_description': 0640,
    #             'owner': 0640,
    #             'group': 0600,
    #             'slug': 0400},
    #         'methods':
    #             {'PUT': '-r-x------',
    #              'GET': '-r-xr-xr-x',
    #              'DELETE': '-r-x------',
    #              'POST': '-r-x------'}
    #         },
    #     'children': ['entry', 'resource'],

    # },
    # 'resource': {
    #     'app': 'badges',
    #     'model': 'Resource',
    #     'factory': 'ResourceFactory',
    #     'parentfield': 'challenge'
    # },
    # 'tag': {
    #     'app': 'badges',
    #     'model': 'Tag',
    #     'factory': 'TagFactory'
    # },
    # 'tool': {
    #     'app': 'badges',
    #     'model': 'tool',
    #     'factory': 'ToolFactory'
    # },
    # 'entry': {
    #     'app': 'badges',
    #     'model': 'Entry',
    #     'factory': 'EntryFactory'
    }
}
