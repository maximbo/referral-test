from typing import Any, cast
from unittest.mock import patch

from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from backend.coupons import services as coupons_services
from .auth_backend import PhoneBackend
from .models import User


class BaseTestCase(APITestCase):
    TEST_PHONE_NUMBER = "+7-987-113-69-28"
    TEST_PHONE_CODE = "0000"

    def create_test_user(self):
        return User.objects.create_user(phone_number=self.TEST_PHONE_NUMBER)  # type: ignore

    def create_test_user_and_login(self):
        user = self.create_test_user()
        self.client.login(
            phone_number=self.TEST_PHONE_NUMBER,
            code=self.TEST_PHONE_CODE,
        )
        return user


class LoginByPhoneTestCase(BaseTestCase):
    def test_success(self):
        url = reverse("users:login-by-phone")
        data = {"phone_number": self.TEST_PHONE_NUMBER}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_invalid_phone(self):
        url = reverse("users:login-by-phone")
        data = {"phone_number": "+7-987-913-69-2"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class CheckPhoneCodeTestCase(BaseTestCase):
    def test_user_created(self):
        url = reverse("users:check-phone-code")
        data = {
            "phone_number": self.TEST_PHONE_NUMBER,
            "code": self.TEST_PHONE_CODE,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)

    def test_user_logged_in(self):
        self.create_test_user()

        url = reverse("users:check-phone-code")
        data = {
            "phone_number": self.TEST_PHONE_NUMBER,
            "code": self.TEST_PHONE_CODE,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(User.objects.count(), 1)

    def test_coupon_created(self):
        url = reverse("users:check-phone-code")
        data = {
            "phone_number": self.TEST_PHONE_NUMBER,
            "code": self.TEST_PHONE_CODE,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = User.objects.get()
        self.assertIsNotNone(user.owned_coupon)  # type: ignore

    def test_user_authenticated(self):
        url = reverse("users:check-phone-code")
        data = {
            "phone_number": self.TEST_PHONE_NUMBER,
            "code": self.TEST_PHONE_CODE,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(response.cookies.get("csrftoken", None))
        self.assertIsNotNone(response.cookies.get("sessionid", None))

    def test_user_is_active(self):
        url = reverse("users:check-phone-code")
        data = {
            "phone_number": self.TEST_PHONE_NUMBER,
            "code": self.TEST_PHONE_CODE,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = User.objects.get()
        self.assertTrue(user.is_active)

    def test_invalid_code_format(self):
        url = reverse("users:check-phone-code")
        data = {
            "phone_number": self.TEST_PHONE_NUMBER,
            "code": "000",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_phone_number_format(self):
        url = reverse("users:check-phone-code")
        data = {"phone_number": "+7-987-913-69-2", "code": "0000"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch.object(PhoneBackend, "is_code_valid")
    def test_invalid_code(self, mock_is_code_valid):
        mock_is_code_valid.return_value = False

        url = reverse("users:check-phone-code")
        data = {
            "phone_number": self.TEST_PHONE_NUMBER,
            "code": "0000",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class LogoutTestCase(BaseTestCase):
    def test_success(self):
        self.create_test_user_and_login()

        url = reverse("users:logout")
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(reverse("users:my-profile"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_failure_not_logged_in(self):
        url = reverse("users:logout")
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class MyProfileTestCase(BaseTestCase):
    def test_success(self):
        self.create_test_user_and_login()

        url = reverse("users:my-profile")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_failure_forbidden(self):
        self.create_test_user()

        url = reverse("users:my-profile")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_subscribed_users(self):
        user = self.create_test_user_and_login()
        coupons_services.activate_coupon(user.owned_coupon)

        for i in range(200, 210):
            coupons_services.subscribe_user_to_coupon(
                User.objects.create_user(  # type: ignore
                    phone_number=f"+7-987-{i}-69-28"
                ),
                user.owned_coupon,
            )

        url = reverse("users:my-profile")
        response = self.client.get(url)

        data: dict[Any, Any] = cast(dict[Any, Any], response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data["subscribed_users"]), 10)
