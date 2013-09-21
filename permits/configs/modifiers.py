from permits import FULL_PERMISSIONS, NARROW_PERMISSIONS


def full_config(group=None):
    if group and group in FULL_PERMISSIONS:
        return FULL_PERMISSIONS[group]
    else:
        return FULL_PERMISSIONS['BASE']


def narrow_config(group):
    if group and group in NARROW_PERMISSIONS:
        return NARROW_PERMISSIONS[group]
    else:
        return NARROW_PERMISSIONS['BASE']
