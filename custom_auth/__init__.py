from django.db import models
from django.contrib.auth.models import Group

if not hasattr(Group, 'parent'):
    field = models.ForeignKey(Group, blank=True, null=True, related_name='children')
    field.contribute_to_class(Group, 'parent')