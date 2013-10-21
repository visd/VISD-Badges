import cPickle as pickle
import os

from django.conf import settings


def load(p):
    if p == 'trav':
        fp = 'permits/configs/traversals.py'
    elif p == 'narrow':
        fp = 'permits/configs/narrow.py'
    elif p == 'full':
        fp = 'permits/configs/full.py'
    with open(os.path.join(settings.PROJECT_ROOT, fp), 'r') as f:
        d = pickle.load(f)
    return d

FULL_PERMISSIONS = load('full')

NARROW_PERMISSIONS = load('narrow')

TRAVERSAL_PERMISSIONS = load('trav')
