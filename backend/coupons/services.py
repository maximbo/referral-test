from django.utils import timezone
from .models import User, Coupon


class CouponAlreadyActivated(Exception): ...


class UserAlreadySubscribedToCoupon(Exception): ...


class CannotSubscribeToOwnCoupon(Exception): ...


class CannotSubscribeToUnactiveCoupon(Exception): ...


def create_coupon_for_user(user: User) -> Coupon:
    return Coupon.objects.create(owner=user)


def activate_coupon(coupon: Coupon, save=True):
    if coupon.activated_on:
        raise CouponAlreadyActivated

    coupon.activated_on = timezone.now()
    if save:
        coupon.save()


def subscribe_user_to_coupon(
    user: User,
    coupon: Coupon,
    save=True,
):
    if coupon.owner_id == user.pk:  # type: ignore
        raise CannotSubscribeToOwnCoupon

    if not coupon.activated_on:
        raise CannotSubscribeToUnactiveCoupon

    if coupon.subscribed_users.filter(pk=user.pk).exists():
        raise UserAlreadySubscribedToCoupon

    coupon.subscribed_users.add(user)
