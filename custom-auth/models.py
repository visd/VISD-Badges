from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

# Create your models here.

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


class UserProfile(AbstractBaseUser, PermissionsMixin):
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

