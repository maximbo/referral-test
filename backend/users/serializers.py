from typing import Any

from rest_framework import serializers
from drf_spectacular.utils import extend_schema_serializer

from phonenumber_field.serializerfields import PhoneNumberField

from .models import User


@extend_schema_serializer(component_name="Входные данные для номера телефона")
class LoginByPhoneIn(serializers.Serializer):
    phone_number = PhoneNumberField()


@extend_schema_serializer(
    component_name="Входные данные для проверка телефона и кода активации"
)
class CheckPhoneCodeIn(serializers.Serializer):
    phone_number = PhoneNumberField()
    code = serializers.CharField(
        min_length=4,
        max_length=4,
        label="Код активации",
    )


@extend_schema_serializer(
    component_name="Выходные данные после регистрации или входа пользователя"
)
class UserLoginOut(serializers.ModelSerializer):
    coupon_code = serializers.SerializerMethodField()
    coupon_code_activated = serializers.SerializerMethodField()

    @staticmethod
    def get_coupon_code(obj: User) -> str:
        return obj.owned_coupon.code  # type: ignore

    @staticmethod
    def get_coupon_code_activated(obj: User) -> bool:
        return obj.owned_coupon.activated_on is not None  # type: ignore

    class Meta:  # type: ignore
        model = User
        fields = [
            "id",
            "phone_number",
            "date_joined",
            "coupon_code",
            "coupon_code_activated",
        ]


@extend_schema_serializer(
    component_name="Выходные данные для профиля пользователя",
)
class UserPrivateProfileOut(serializers.ModelSerializer):
    class SubscribedUser(serializers.ModelSerializer):
        class Meta:  # type: ignore
            model = User
            fields = ["phone_number"]

    coupon_code = serializers.SerializerMethodField()
    coupon_code_activated = serializers.SerializerMethodField()
    subscribed_users = serializers.SerializerMethodField()

    class Meta:  # type: ignore
        model = User
        fields = [
            "id",
            "phone_number",
            "date_joined",
            "coupon_code",
            "coupon_code_activated",
            "subscribed_users",
        ]

    @staticmethod
    def get_coupon_code(obj: User) -> str:
        return obj.owned_coupon.code  # type: ignore

    @staticmethod
    def get_coupon_code_activated(obj: User) -> bool:
        return obj.owned_coupon.activated_on is not None  # type: ignore

    def get_subscribed_users(self, obj: User) -> dict[Any, Any]:
        subscribed_users = self.context["subscribed_users"]
        return self.SubscribedUser(subscribed_users, many=True).data
