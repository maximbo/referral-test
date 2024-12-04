from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    def get_queryset(self):
        return super().get_queryset().prefetch_related("owned_coupon")

    def create_user(
        self,
        phone_number: str,
        **extra_fields,
    ):
        from .services import create_user

        if not phone_number:
            raise ValueError(_("The phone number must be set"))

        return create_user(phone_number, **extra_fields)

    def create_superuser(
        self,
        phone_number: str,
        **extra_fields,
    ):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))

        return self.create_user(phone_number, **extra_fields)
