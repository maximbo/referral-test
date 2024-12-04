from .models import User


def create_user(phone_number: str, save=True, **extra_fields):
    from backend.coupons.services import create_coupon_for_user

    user = User(phone_number=phone_number, **extra_fields)

    if save:
        user.save()

    create_coupon_for_user(user)

    return user
