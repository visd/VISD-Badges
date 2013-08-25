RESOURCE_CONFIGS = {

    'challenge': {
        'app': 'badges',
        'model': 'Challenge',
        'factory': 'ChallengeFactory',
        'parentfield': 'skill'
    },
    'skillset': {
        'app': 'badges',
        'model': 'Skillset',
        'factory': 'SkillsetFactory'
    },
    'resource': {
        'app': 'badges',
        'model': 'Resource',
        'factory': 'ResourceFactory',
        'parentfield': 'challenge'
    },
    'tag': {
        'app': 'badges',
        'model': 'Tag',
        'factory': 'TagFactory'
    },
    'tool': {
        'app': 'badges',
        'model': 'Tool',
        'factory': 'ToolFactory'
    },
    'entry': {
        'app': 'badges',
        'model': 'Entry',
        'factory': 'EntryFactory'
    },
    'user': {
        'app': 'auth',
        'model': 'User',
        'factory': 'UserFactory'
    },
    'group': {
        'app': 'auth',
        'model': 'Group',
        'factory': 'GroupFactory'
    }
}

def deverbose(verbose_name):
    return RESOURCE_CONFIGS[{
        'challenges':'challenge',
        'skillsets':'skillset',
        'resources':'resource',
        'tags':'tag',
        'tools':'tool',
        'entries':'entry',
        'users':'user',
        'groups':'group',
        'index':'index'
    }[verbose_name]]