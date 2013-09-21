import cPickle as pickle

FULL_PERMISSIONS = pickle.load(open('permits/configs/full.py', 'r'))

NARROW_PERMISSIONS = pickle.load(open('permits/configs/narrow.py', 'r'))