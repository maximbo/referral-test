from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from .models import User
from backend.users import services as users_services
from . import services


class BaseTestCase(APITestCase):
    TEST_PHONE_NUMBER = "+7-987-113-69-28"
    TEST_PHONE_CODE = "0000"

    def create_test_user(self):
        return users_services.create_user(self.TEST_PHONE_NUMBER)

    def create_test_user_and_login(self):
        user = self.create_test_user()
        self.client.login(
            phone_number=self.TEST_PHONE_NUMBER,
            code=self.TEST_PHONE_CODE,
        )
        return user


class ActivateMyCouponTestCase(BaseTestCase):
    def test_success(self):
        user = self.create_test_user_and_login()

        url = reverse("coupons:activate-my-coupon")
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        user = User.objects.get(pk=user.pk)
        self.assertTrue(user.owned_coupon.activated_on)

    def test_reactivation_failure(self):
        user = self.create_test_user_and_login()

        url = reverse("coupons:activate-my-coupon")
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        user = User.objects.get(pk=user.pk)
        self.assertTrue(user.owned_coupon.activated_on)

        url = reverse("coupons:activate-my-coupon")
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class SubscribeUserByCouponTestCase(BaseTestCase):
    def test_success(self):
        current_user = self.create_test_user_and_login()

        phone_number = "+7-987-113-70-28"
        another_user = users_services.create_user(phone_number)
        services.activate_coupon(another_user.owned_coupon)

        url = reverse(
            "coupons:subscribe-user-to-coupon",
            kwargs={"coupon_code": another_user.owned_coupon.code},
        )
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(another_user.owned_coupon.subscribed_users.count(), 1)
        self.assertEqual(current_user.connected_coupons.count(), 1)

    def test_failure_coupon_does_not_exists(self):
        self.create_test_user_and_login()

        phone_number = "+7-987-113-70-28"
        another_user = users_services.create_user(phone_number)

        url = reverse(
            "coupons:subscribe-user-to-coupon",
            kwargs={"coupon_code": another_user.owned_coupon.code},
        )
        another_user.owned_coupon.delete()
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_failure_coupon_not_activated(self):
        self.create_test_user_and_login()

        phone_number = "+7-987-113-70-28"
        another_user = users_services.create_user(phone_number)

        url = reverse(
            "coupons:subscribe-user-to-coupon",
            kwargs={"coupon_code": another_user.owned_coupon.code},
        )
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_failure_cannot_subscribe_to_own_coupon(self):
        user = self.create_test_user_and_login()
        services.activate_coupon(user.owned_coupon)

        phone_number = "+7-987-113-70-28"

        url = reverse(
            "coupons:subscribe-user-to-coupon",
            kwargs={"coupon_code": user.owned_coupon.code},
        )
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_already_subscribed(self):
        current_user = self.create_test_user_and_login()

        phone_number = "+7-987-113-70-28"
        another_user = users_services.create_user(phone_number)
        services.activate_coupon(another_user.owned_coupon)

        url = reverse(
            "coupons:subscribe-user-to-coupon",
            kwargs={"coupon_code": another_user.owned_coupon.code},
        )
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(another_user.owned_coupon.subscribed_users.count(), 1)
        self.assertEqual(current_user.connected_coupons.count(), 1)

        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(another_user.owned_coupon.subscribed_users.count(), 1)
        self.assertEqual(current_user.connected_coupons.count(), 1)


class CheckCouponPresenceTestCase(BaseTestCase):
    def test_success(self):
        user = self.create_test_user_and_login()
        services.activate_coupon(user.owned_coupon)

        url = reverse(
            "coupons:check-coupon-presence",
            kwargs={"coupon_code": user.owned_coupon.code},
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_coupon_not_found(self):
        self.create_test_user_and_login()

        url = reverse(
            "coupons:check-coupon-presence",
            kwargs={"coupon_code": "ffffff"},
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_coupon_not_activated(self):
        user = self.create_test_user_and_login()

        url = reverse(
            "coupons:check-coupon-presence",
            kwargs={"coupon_code": user.owned_coupon.code},
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_another_user_coupon(self):
        self.create_test_user_and_login()

        phone_number = "+7-987-113-70-28"
        another_user = users_services.create_user(phone_number)
        services.activate_coupon(another_user.owned_coupon)

        url = reverse(
            "coupons:check-coupon-presence",
            kwargs={"coupon_code": another_user.owned_coupon.code},
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_another_user_coupon_not_activated(self):
        self.create_test_user_and_login()

        phone_number = "+7-987-113-70-28"
        another_user = users_services.create_user(phone_number)

        url = reverse(
            "coupons:check-coupon-presence",
            kwargs={"coupon_code": another_user.owned_coupon.code},
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
