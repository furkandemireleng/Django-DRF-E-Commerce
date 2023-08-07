from django.db import models

# Create your models here.
from datetime import date

from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
import random
import string
import os


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('name', "Furkan")
        extra_fields.setdefault('surname', "Demirel")
        extra_fields.setdefault('id_number', "36445290668")
        extra_fields.setdefault('phoneNumber', "905316564601")
        extra_fields.setdefault('country', "Turkey")
        extra_fields.setdefault('city', "Istanbul")
        extra_fields.setdefault('zipCode', "34000")
        extra_fields.setdefault('address', "Medrese Ali Bey mah. izzet bey 1. sokak tekin apt no:6/7")
        return self.create_user(email, password, **extra_fields)


def get_image_upload_path(instance, filename):
    random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    random_num = random.randint(100, 999)
    basename, extension = os.path.splitext(filename)
    filename = f"profile-{random_str}{random_num}{extension}"
    return f"images/profile/{instance.cowork.id}/{instance.branch.id}/{instance.id}/{filename}"


class Profile(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True, db_index=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_guest = models.BooleanField(default=False)
    date_joined = models.DateField(default=timezone.now)
    date_of_birth = models.DateField(default=timezone.now)
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    id_number = models.CharField(max_length=28, unique=True)
    phoneNumber = models.CharField(max_length=13, verbose_name="Phone number", unique=True)
    country = models.CharField(max_length=28)
    city = models.CharField(max_length=28)
    zipCode = models.CharField(max_length=5)
    address = models.CharField(max_length=150, verbose_name="User Address")

    def validate_image(fieldfile_obj):
        filesize = fieldfile_obj.file.size
        megabyte_limit = 5.0
        if filesize > megabyte_limit * 1024 * 1024:
            raise ValidationError("Max file size is %sMB" % str(megabyte_limit))

    profile_image = models.ImageField(
        upload_to=get_image_upload_path,
        validators=[validate_image],
        verbose_name="profile_image",
        null=True,
        blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
