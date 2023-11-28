from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone


class AccountManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        email = self.normalize_email(email)

        user: Account = self.model(
            email=email,
            **kwargs,
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **kwargs):
        user = self.create_user(email=email, password=password, is_active=True, is_superuser=True, **kwargs)
        user.save()
        return user


class Account(AbstractBaseUser, PermissionsMixin):
    class Role(models.TextChoices):
        SUPERADMIN = 'Superadmin', 'superadmin'
        ADMIN = 'Admin', 'admin'
        MEMBER = 'Member', 'member'

    email = models.EmailField(blank=False, null=False, unique=True, db_index=True)
    username = models.CharField(max_length=128, blank=False, null=False, unique=True, db_index=True)
    role = models.CharField(max_length=15, choices=Role.choices, default=Role.MEMBER)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    objects = AccountManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'role']

    @property
    def is_staff(self) -> bool:
        return self.role in [self.Role.SUPERADMIN, self.Role.ADMIN]

    def __str__(self) -> str:
        return f'Account(email={self.email}, username={self.username}, role={self.role})'

    class Meta:
        db_table = 'accounts'
