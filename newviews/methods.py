"""
The job of these methods is to contruct a dictionary 

Views are constructed from the intersection of the desired fields in the  
"""

from permissions import methods as permissions_methods

METHODS_MAP = {
    'GET': 'read',
    'PUT': 'write',
    'DELETE': 'write',
    'POST': 'write'
}


def get_fields_from(inst, fields):
    """ Accepts a model instance and a list of fields to lookup on that instance.

    Returns a dictionary from the fields.
    """
    return {f:getattr(inst,f) for f in fields}


def remove_blacklist(blacklist, whitelist):
    """ Returns the intersection of two lists. A simple utility.

    >>> print 
    """
    return list(set(whitelist)-set(blacklist))

def fetch_view(resource,method,view_type):
    """Example arguments:
    ('Challenge','GET','detail')

    We assume that everything is permitted. We will optionally throttle all these methods
    via table- and column-level permissions.
    """
    # We can assume the user has permission
    


# def retrieve(set, inst):
#     """ Returns a target set of attributes and a model instance.

#     Fetches the set from BASE_RESOURCES, so it had better be there.
#     """
#     view = BASE_RESOURCES[inst._meta.verbose_name][set]
#     result = get_fields_from(inst,view['fields'])
#     return result