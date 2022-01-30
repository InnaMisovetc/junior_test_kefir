from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models


class CityModel(models.Model):
    name = models.CharField(max_length=150)


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifier
    for authentication instead of username.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(verbose_name='First Name', max_length=150, blank=False, null=False)
    last_name = models.CharField(verbose_name='Last Name', max_length=150, blank=False, null=False)
    other_name = models.CharField(verbose_name='Other Name', max_length=150, blank=True, null=True)
    email = models.EmailField(unique=True, blank=False, null=False)
    phone = models.CharField(max_length=20, blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    city = models.ForeignKey(CityModel, on_delete=models.SET_NULL, null=True)
    additional_info = models.TextField(null=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    objects = CustomUserManager()
