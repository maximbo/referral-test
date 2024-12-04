from django.urls import path, register_converter

from . import api


class CouponCodeConverter:
    regex = r"[\w\d]{6}"

    def to_python(self, value):
        return str(value)

    def to_url(self, value):
        return str(value)


register_converter(CouponCodeConverter, "coupon_code")

app_name = "coupons"

urlpatterns = [
    path(
        "mine/activate",
        api.activate_my_coupon,
        name="activate-my-coupon",
    ),
    path(
        "<coupon_code:coupon_code>/subscribe",
        api.subscribe_user_to_coupon,
        name="subscribe-user-to-coupon",
    ),
    path(
        "<coupon_code:coupon_code>/check",
        api.check_coupon_presence,
        name="check-coupon-presence",
    ),
]
