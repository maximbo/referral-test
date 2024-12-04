import time

from django.contrib.auth import authenticate, login, logout

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.permissions import IsAuthenticated

from drf_spectacular.utils import extend_schema, OpenApiResponse


from .models import User
from . import serializers


@extend_schema(
    operation_id="users:login-by-phone",
    request=serializers.LoginByPhoneIn,
    responses={
        status.HTTP_201_CREATED: OpenApiResponse(
            description="Пользователю отправлено сообщение для входа"
        ),
        status.HTTP_400_BAD_REQUEST: OpenApiResponse(
            description="Ошибка валидации данных"
        ),
    },
)
@api_view(["POST"])
@authentication_classes([])
@permission_classes([])
def login_by_phone(request: Request) -> Response:
    """
    Авторизация по номеру телефона.
    """

    serializer = serializers.LoginByPhoneIn(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    time.sleep(0.5)

    return Response(
        {"detail": "Код авторизации отослан"},
        status=status.HTTP_201_CREATED,
    )


@extend_schema(
    operation_id="users:check-phone-code",
    request=serializers.CheckPhoneCodeIn,
    responses={
        status.HTTP_200_OK: OpenApiResponse(
            response=serializers.UserLoginOut,
            description="Пользователь авторизован",
        ),
        status.HTTP_201_CREATED: OpenApiResponse(
            response=serializers.UserLoginOut,
            description="Пользователь зарегистрирован",
        ),
        status.HTTP_400_BAD_REQUEST: OpenApiResponse(
            description="Ошибка валидации данных"
        ),
        status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
            description="Неверный телефон или проверочный код"
        ),
    },
)
@api_view(["POST"])
@authentication_classes([])
@permission_classes([])
def check_phone_code(request: Request) -> Response:
    """
    Проверка кода для авторизации по номеру телефона.
    """

    serializer = serializers.CheckPhoneCodeIn(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    phone_number = serializer.validated_data["phone_number"]
    code = serializer.validated_data["code"]

    user_exists = User.objects.filter(phone_number=phone_number).exists()
    user = authenticate(request, username=phone_number, code=code)

    if user is None:
        return Response(
            {"detail": "Неверный код подтверждения"},
            status.HTTP_401_UNAUTHORIZED,
        )

    login(request, user)

    if user_exists:
        return Response(
            serializers.UserLoginOut(user).data,
            status=status.HTTP_200_OK,
        )

    return Response(
        serializers.UserLoginOut(user).data,
        status=status.HTTP_201_CREATED,
    )


@extend_schema(
    operation_id="users:logout",
    request=None,
    responses={
        status.HTTP_200_OK: OpenApiResponse(
            description="Пользователь разлогинен",
        )
    },
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout_user(request: Request) -> Response:
    """
    Разлогинить пользователя.
    """

    logout(request)
    return Response({"detail": "Пользователь разлогинен"}, status.HTTP_200_OK)


@extend_schema(
    operation_id="users:get-my-profile",
    request=None,
    responses={
        status.HTTP_200_OK: OpenApiResponse(
            serializers.UserPrivateProfileOut,
        )
    },
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user_self_profile(request: Request) -> Response:
    """
    Показать пользователю его профиль
    """

    subscribed_users = request.user.owned_coupon.subscribed_users.all().only(
        "phone_number"
    )  # type: ignore

    serializer = serializers.UserPrivateProfileOut(
        request.user,
        context={"subscribed_users": subscribed_users},
    )

    return Response(serializer.data, status.HTTP_200_OK)
