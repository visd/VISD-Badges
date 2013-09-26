import cPickle as pickle


def load(p):
    if p == 'trav':
        f = open('permits/configs/traversals.py', 'r')
    elif p == 'narrow':
        f = open('permits/configs/narrow.py', 'r')
    elif p == 'full':
        f = open('permits/configs/full.py', 'r')
    d = pickle.load(f)
    f.close()
    return d

FULL_PERMISSIONS = load('full')

NARROW_PERMISSIONS = load('narrow')

TRAVERSAL_PERMISSIONS = load('trav')
