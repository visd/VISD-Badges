RESOURCE_CONFIGS = {

    'challenge': {
        'app': 'badges',
        'model': 'Challenge',
        'factory': 'ChallengeFactory',
        'parentfield': 'skill',
        'description': 'Challenges represent projects or ideas teachers can take on.'
    },
    'skillset': {
        'app': 'badges',
        'model': 'Skillset',
        'factory': 'SkillsetFactory',
        'description': 'Skillsets are areas of strength that teachers can build on.'
    },
    'resource': {
        'app': 'badges',
        'model': 'Resource',
        'factory': 'ResourceFactory',
        'parentfield': 'challenge',
        'description': 'More information about a challenge, usually as a link to a website.'
    },
    'tag': {
        'app': 'badges',
        'model': 'Tag',
        'factory': 'TagFactory',
        'description': 'Tags let users mark entries, challenges or other objects with a keyword.'
    },
    'tool': {
        'app': 'badges',
        'model': 'Tool',
        'factory': 'ToolFactory',
        'description': 'Cameras, software, devices -- anything a teacher uses in an entry.'
    },
    'entry': {
        'app': 'badges',
        'model': 'Entry',
        'factory': 'EntryFactory',
        'description': 'A way to submit an example of your work. Entries show you have completed a challenge.'
    },
    'user': {
        'app': 'auth',
        'model': 'User',
        'factory': 'UserFactory',
        'description': 'A user in the system. You must be logged in to show up as a user.'
    },
    'group': {
        'app': 'auth',
        'model': 'Group',
        'factory': 'GroupFactory',
        'description': 'Groups gain different kinds of access to objects that belong to their group.'
    },
    'event': {
        'app': 'events',
        'model': 'Event',
        'factory': 'EventFactory',
        'description': 'Events mark what is happening in the system. The user sees what is happening in his/her group, or system-wide.'
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
        'index':'index',
        'events':'event'
    }[verbose_name]]