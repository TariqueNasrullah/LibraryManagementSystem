from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.utils import timezone

'''
CustomAccountManager implements BaseUserManager that enables
Django to user email field for login, instead of username
'''


class CustomAccountManager(BaseUserManager):
    # create_user creates an user with unprivileged access and save it to storage
    def create_user(self, email, username, first_name, password, **other_fields):
        if not email:
            raise ValueError(_('You must provide an email address'))
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, first_name=first_name, **other_fields)

        user.set_password(password)
        user.save()

        return user

    # create_superuser creates an user with privileged access and save it to storage
    def create_superuser(self, email, username, first_name, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, username, first_name, password, **other_fields)


# CustomUser custom model that support avatar image field
class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    avatar = models.ImageField(upload_to='images', blank=True)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name']

    def __str__(self):
        return self.username
