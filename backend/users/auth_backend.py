from django.http import HttpRequest
from django.contrib.auth.backends import ModelBackend
from .models import User


class PhoneBackend(ModelBackend):
    def authenticate(  # type: ignore
        self,
        request: HttpRequest,
        username: str | None = None,
        code: str | None = None,
        **kwargs,
    ):
        if username is None:
            username = kwargs.get(User.USERNAME_FIELD)

        if username is None or code is None:
            return

        if not self.is_code_valid(username, code):
            return

        try:
            user = User.objects.get(phone_number=username)
        except User.DoesNotExist:
            user = User.objects.create_user(phone_number=username)  # type: ignore

        if self.user_can_authenticate(user):
            return user

    def is_code_valid(self, username: str, code: str) -> bool:
        return True
