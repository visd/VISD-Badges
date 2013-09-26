def retrieve(set, inst):
    """ Returns a target set of attributes and a model instance.

    Fetches the set from BASE_RESOURCES, so it had better be there.
    """
    view = BASE_RESOURCES[inst._meta.verbose_name][set]
    result = get_fields_from(inst,view['fields'])
    return result