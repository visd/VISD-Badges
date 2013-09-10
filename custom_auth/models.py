from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin,\
Group, Permission
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from badges.model_mixins import URLmixin


class CustomUserManager(BaseUserManager):
    """docstring for CustomUserManager"""

    def _create_user(self, email, first_name, last_name, password,
                         is_staff, is_superuser, **extra_fields):
            """
            Creates and saves a User with the given username, email and password.
            """
            now = timezone.now()
            if not email:
                raise ValueError('The given users email must be set')
            email = self.normalize_email(email)
            user = self.model(email=email,
                              first_name=first_name,
                              last_name=last_name,
                              is_staff=is_staff,
                              is_active=True,
                              is_superuser=is_superuser,
                              last_login=now,
                              date_joined=now,
                              **extra_fields)
            user.set_password(password)
            user.save(using=self._db)
            return user
    
    def create_user(self, email, first_name, last_name, password, **extra_fields):
        return self._create_user(email, first_name=first_name, last_name=last_name, 
                                 password=password, is_staff=False, is_superuser=False, **extra_fields)
        
    def create_superuser(self, email, first_name, last_name, password, **extra_fields):
        return self._create_user(email, first_name=first_name, last_name=last_name,
                                 password=password, is_staff=True, is_superuser=True, **extra_fields)
    
    def get_by_natural_key(self, email):
        return self.get(**{self.model.USERNAME_FIELD: email})


class CustomUser(AbstractBaseUser, PermissionsMixin, URLmixin):
    """An extended User with more fields"""

    USERNAME_FIELD='email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=60, db_index=True, unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    is_staff = models.BooleanField(_('staff status'), default=False,
            help_text=_('Designates whether the user can log into this admin '
                        'site.'))
    is_active = models.BooleanField(_('active'), default=True,
            help_text=_('Designates whether this user should be treated as '
                        'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    memberships = models.ManyToManyField('NestedGroup', related_name='users')

    objects = CustomUserManager()

    def get_full_name(self):
            """
            Returns the first_name plus the last_name, with a space in between.
            """
            full_name = '%s %s' % (self.first_name, self.last_name)
            return full_name.strip()

    def get_short_name(self):
            "Returns the short name for the user."
            return self.first_name

    def email_user(self, subject, message, from_email=None):
            """
            Sends an email to this User.
            """
            send_mail(subject, message, from_email, [self.email])

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')


class NestedGroupManager(models.Manager):
    """
    The manager for the Group model. Because the NestedGroup has parents, this manager can
    return a tree of groups, get a group and all its children, and so on.
    """
    family_tree = {}

    def get_by_name(self, name):
        return self.get(name=name)

    def get_group_and_children(self, pk):
        pass

    def access_as(self, user_group, obj_group):
        """ Can a user of user_group access an object of obj_group?
            True of False.
        """
        return obj_group in self.all_children_of(user_group) or user_group == obj_group

    def all_children_of(self, name):
        if not self.family_tree.get(name):
            self.family_tree[name] = []
            self.walk_children_of(name) 
        return self.family_tree[name]

    def top_groups(self, group_list):
        """ Given a list of groups, returns the groups which have no parents in the list.
            Notice that, since we may be dealing with disjoint trees, we return a tuple of top groups.
        """
        child_set = set([])
        for group in group_list:
            child_set = child_set | set(self.all_children_of(group))
        return tuple(set(group_list)-child_set)

    def walk_children_of(self, name, head=None):
        top_group = head or name
        g = self.get(name=name)
        if g.children.count():
            for child in g.children.all():
                self.family_tree[top_group].append(child.name)
                self.walk_children_of(child, head=top_group)
        return

    def create_group(self, name, parent):
        pass

class NestedGroup(Group):
    """
    Look in this app's __init__.py to see how we add a 'parent' field to the built-in
    Group. Otherwise this is a proxy model for adding
    """
    objects = NestedGroupManager()

    class Meta:
        proxy = True
        verbose_name = _('group')
        verbose_name_plural = _('groups')

    def __str__(self):
        return self.name

    def natural_key(self):
        return (self.name,)
