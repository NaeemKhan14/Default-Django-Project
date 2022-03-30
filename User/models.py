import string
import random

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin, Group
from django.db import models
from django.utils import timezone


class AccountManager(BaseUserManager):

    def create_user(self, email, username, password, **other_fields):

        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("Users must have an unique username")

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **other_fields)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, username, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)
        other_fields.setdefault('is_admin', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('is_staff flag cannot be False')
        if other_fields.get('is_superuser') is not True:
            raise ValueError('is_superuser flag cannot be False')
        # Assign a random salary number for super user
        other_fields['salary_num'] = ''.join(random.choices(string.ascii_uppercase + string.digits, k=20))
        # Save the user model
        user = self.create_user(email, username, password, **other_fields)

        return user


class UserAccount(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=30, unique=True, verbose_name='Username')
    email = models.EmailField(max_length=60, unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    salary_num = models.CharField(max_length=30, unique=True, verbose_name='Salary Number')
    last_login = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True, verbose_name='Status')
    is_moderator = models.BooleanField(default=False, verbose_name='Permissions')
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    is_superuser = models.BooleanField(default=False)
    projects = models.ManyToManyField('Project.Project', related_name='user_projects', blank=True)

    objects = AccountManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

