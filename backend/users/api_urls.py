from django.urls import path

from . import api

app_name = "users"

urlpatterns = [
    path(
        "login-by-phone/",
        api.login_by_phone,
        name="login-by-phone",
    ),
    path(
        "check-phone-code/",
        api.check_phone_code,
        name="check-phone-code",
    ),
    path(
        "logout/",
        api.logout_user,
        name="logout",
    ),
    path(
        "me/",
        api.get_user_self_profile,
        name="my-profile",
    ),
]
