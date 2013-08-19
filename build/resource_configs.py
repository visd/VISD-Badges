BASE_RESOURCES = {

    'challenge': {
        'app': 'badges',
        'model': 'Challenge',
        'factory': 'ChallengeFactory',
        'parentfield': 'skill'
    }
}


# 'skillset': {
#         'app': 'badges',
#         'model': 'Skillset',
#         'factory': 'SkillsetFactory'
#     },
#     'resource': {
#         'app': 'badges',
#         'model': 'Resource',
#         'factory': 'ResourceFactory',
#         'parentfield': 'challenge'
#     },
#     'tag': {
#         'app': 'badges',
#         'model': 'Tag',
#         'factory': 'TagFactory'
#     },
#     'tool': {
#         'app': 'badges',
#         'model': 'tool',
#         'factory': 'ToolFactory'
#     },
#     'entry': {
#         'app': 'badges',
#         'model': 'Entry',
#         'factory': 'EntryFactory'
#     }