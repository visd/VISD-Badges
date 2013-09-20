import itertools

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from custom.utils import memoized_property
from badges.model_mixins import URLmixin


class CustomUserManager(BaseUserManager):
    """docstring for CustomUserManager"""

    use_for_related_fields = True

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

    def url(self, scoped=True):
        parent = self.__dict__.get('instance')
        return '%s/%s' % (scoped and (parent and ('%s' % parent.url)) or "", self.model._meta.verbose_name_plural)


class CustomUser(AbstractBaseUser, URLmixin):
    """An extended User with more fields"""

    USERNAME_FIELD='email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    group = models.ForeignKey('NestedGroup', related_name='users', null=True)
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
    memberships = models.ManyToManyField('NestedGroup', related_name='members')

    collection = CustomUserManager()
    objects = models.Manager()

    @memoized_property
    def user(self):
        return self

    @memoized_property
    def user_id(self):
        return self.id

    @memoized_property
    def parent_instance(self):
        return None

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

    @memoized_property
    def all_groups(self):
        manager = self.memberships
        return list(itertools.chain(
                    *[manager.children_and_self_of(g)
                      for g in
                      manager.only('name', 'parent').all()]
                    )
                    )

    @memoized_property
    def all_group_ids(self):
        manager = self.memberships
        return list(itertools.chain(
                    *[manager.all_children_ids(g)
                      for g in
                      manager.only('name', 'parent').all()]
                    )
                    )

    def status_over(self, target_group):
        """ Given a group, what is the highest-status group 
        this user can hold over that group?
        Ex.: A user with 'visd-staff' and a target of 'visd-guest'
        returns 'visd-staff.'
        """
        result = None
        for group in self.memberships.all():
            if set(self.memberships.children_and_self_of(group)) &\
            set(self.memberships.children_and_self_of(target_group)):
                result = group
        return result

    def __unicode__(self):
        return self.get_full_name()

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'


class NestedGroupManager(models.Manager):
    """
    The manager for the Group model. Because the NestedGroup has parents, this manager can
    return a tree of groups, get a group and all its children, and so on.
    """
    family_tree = {}

    use_for_related_fields = True

    def _walk_children_of(self, this_group, head=None):
        """ accepts and returns group instances.
        """
        top_group = head or this_group
        if this_group.children.count():
            for child in this_group.children.all():
                self.family_tree[top_group.name].append(child)
                self._walk_children_of(child, head=top_group)
        return

    # def add(self, *groups):
    #     """ We want to make sure that a group an its ancestor are never together.
    #     """
    #     if len(groups) > 1:
    #         groups = self.top_groups(list(groups))
    #     super(NestedGroupManager, self).add(*groups)

        # for group in groups:
        #     for g in self.all():
        #         if g in self.children_and_self_of(group):
        #             self.remove(g)
        #         if group in self.children_and_self_of(g):
        #             pass



    def get_by_name(self, name):
        return self.get(name=name)

    def get_group_and_children(self, pk):
        pass

    def access_as(self, user_group, obj_group):
        """ Can a user of user_group access an object of obj_group?
            True of False.
        """
        return obj_group in self.children_and_self_of(user_group) or user_group == obj_group

    def only_children_of(self, group):
        name = group.name
        if not self.family_tree.get(name):
            self.family_tree[name] = []
            self._walk_children_of(group)
        return self.family_tree[name]

    def children_and_self_of(self, group):
        """ Also returns the parent in the list.
        """
        return [group] + self.only_children_of(group)

    def all_children_ids(self, group):
        """ Converts children_and_self_of to ids.
        """
        return [g.pk for g in self.children_and_self_of(group)]

    def top_groups(self, group_list):
        """ Given a list of groups, returns the groups which have no parents in the list.
            Notice that, since we may be dealing with disjoint trees, we return a tuple of top groups.
        """
        child_set = set([])
        for group in group_list:
            child_set = child_set | set(self.only_children_of(group))
        return tuple(set(group_list)-child_set)

    def create_group(self, name, parent):
        pass

    def url(self, scoped=True):
        parent = self.__dict__.get('instance')
        return '%s/%s' % (scoped and (parent and ('%s' % parent.url)) or "", self.model._meta.verbose_name_plural)


class NestedGroup(models.Model):
    """
    Lord help us, we broke the admin. No going back now, unless we have to.
    """
    name = models.CharField(max_length=32, primary_key=True)
    parent = models.ForeignKey('self', related_name='children', blank=True, null=True)
    user = models.ForeignKey(CustomUser, related_name='groups', null=True)
    
    objects = NestedGroupManager()

    @memoized_property
    def group(self):
        return self

    @memoized_property
    def group_id(self):
        return self.pk

    @memoized_property
    def parent_instance(self):
        return None

    class Meta:
        verbose_name = 'group'
        verbose_name_plural = 'groups'

    def __unicode__(self):
        return self.name

    def natural_key(self):
        return (self.name,)
