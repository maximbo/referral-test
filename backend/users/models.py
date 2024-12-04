import uuid

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone

from phonenumber_field.modelfields import PhoneNumberField

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone_number = PhoneNumberField(unique=True, blank=False)

    is_staff = models.BooleanField(
        default=False,
        null=False,
    )
    is_active = models.BooleanField(
        default=True,
        null=False,
    )
    date_joined = models.DateTimeField(
        default=timezone.now,
        null=False,
    )

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:  # type: ignore
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"

    def __repr__(self) -> str:
        return str(self.phone_number)

    __str__ = __repr__
