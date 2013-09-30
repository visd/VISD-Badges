from .models import NestedGroup


def build_group_dict(this_group, group_list=None):
    """ accepts and returns group instances.
    """
    group_list = group_list or []
    if this_group.children.count():
        for child in this_group.children.all():
            group_list
            self._walk_children_of(child, head=top_group)

    return child_list
