from .dev import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'knowhowsdb',
        'USER': 'djangodb',
        'PASSWORD': 'rheuvo55'
    }
}

INSTALLED_APPS += ('south',)
