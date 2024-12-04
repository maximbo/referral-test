from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import (
    api_view,
    permission_classes,
)
from rest_framework.permissions import IsAuthenticated

from drf_spectacular.utils import extend_schema, OpenApiResponse

from .models import Coupon
from .serializers import MessageSerializer
from . import services


@extend_schema(
    operation_id="coupons:activate-my-coupon",
    request=None,
    responses={
        status.HTTP_202_ACCEPTED: OpenApiResponse(
            MessageSerializer, description="Купон успешно активирован"
        ),
        status.HTTP_400_BAD_REQUEST: OpenApiResponse(
            MessageSerializer, description="Купон уже был активирован"
        ),
    },
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def activate_my_coupon(request: Request) -> Response:
    """
    Активировать собственный купон.
    """

    coupon: Coupon = request.user.owned_coupon  # type: ignore

    try:
        services.activate_coupon(coupon, save=True)
    except services.CouponAlreadyActivated:
        return Response(
            {"detail": "Купон уже активирован"},
            status.HTTP_400_BAD_REQUEST,
        )

    return Response({"detail": "Купон активирован"}, status.HTTP_202_ACCEPTED)


@extend_schema(
    operation_id="coupons:subscribe-user-to-coupon",
    request=None,
    responses={
        status.HTTP_201_CREATED: OpenApiResponse(
            MessageSerializer, description="Пользователь успешно присоединился"
        ),
        status.HTTP_403_FORBIDDEN: OpenApiResponse(
            MessageSerializer, description="Ошибка подписки на пользователя"
        ),
    },
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def subscribe_user_to_coupon(request: Request, coupon_code: str) -> Response:
    """
    Присоединиться к другому пользователю через его купон.
    """

    coupon = get_object_or_404(Coupon, code=coupon_code)

    try:
        services.subscribe_user_to_coupon(request.user, coupon)
    except services.CannotSubscribeToOwnCoupon:
        return Response(
            {"detail": "Невозможно подписаться на собственный купон"},
            status.HTTP_403_FORBIDDEN,
        )
    except services.CannotSubscribeToUnactiveCoupon:
        return Response(
            {"detail": "Купон не активирован"},
            status.HTTP_403_FORBIDDEN,
        )
    except services.UserAlreadySubscribedToCoupon:
        return Response(
            {"detail": "Пользователь уже подписан на этот купон"},
            status.HTTP_403_FORBIDDEN,
        )

    return Response(
        {"detail": "Подписка успешно оформлена"},
        status.HTTP_201_CREATED,
    )


@extend_schema(
    operation_id="coupons:check-coupon-presence",
    request=None,
    responses={
        status.HTTP_200_OK: OpenApiResponse(
            MessageSerializer,
            description="Купон существует и активирован",
        ),
        status.HTTP_404_NOT_FOUND: OpenApiResponse(
            MessageSerializer,
            description="Купон не найден или не активирован",
        ),
    },
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def check_coupon_presence(request: Request, coupon_code: str) -> Response:
    """
    Проверка купона на существование и активацию.
    """

    coupon = get_object_or_404(Coupon, code=coupon_code)

    if not coupon.activated_on:
        return Response(status=status.HTTP_404_NOT_FOUND)

    return Response(status=status.HTTP_200_OK)
