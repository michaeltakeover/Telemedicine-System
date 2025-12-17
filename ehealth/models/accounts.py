
"""
Custom user model and user manager for the telemedicine system.
Authentication is  using email instead of username.
"""
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class UserManager(BaseUserManager):
    """
    Custom user manager that supports email-based authentication.
    """
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Creates and returns a superuser with administrative privileges.
        """

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        return self.create_user(email, password, **extra_fields)

#  USER MODEL (LOGIN ACCOUNT)


class NewUser(AbstractUser):
    """
    Custom user model used for authentication.
    Extends Django's AbstractUser and replaces username with email login.
    """
    username = None
    email = models.EmailField(unique=True)


    ROLES = [
        ("patient", "Patient"),
        ("doctor", "Doctor"),
        ("admin", "Admin"),
    ]
    GENDER_CHOICES = [
        ("male", "Male"), ("female", "Female"), ("other", "Other"),]


    role = models.CharField(max_length=20, choices=ROLES, blank=False, null=False)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(max_length=10,choices=GENDER_CHOICES)

    # normal django User includes:
    # username, first_name, last_name, email, password, is_staff,
    # is_active, is_superuser, last_login, date_joined

    USERNAME_FIELD = "email"  # LOGIN with email
    REQUIRED_FIELDS = []  # No username required

    objects = UserManager()
    #User = get_user_model()

    def __str__(self):
        return f"{self.email} -{self.role}"
