from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from core.tests.config_for_tests import (
    BASE_URL,
    DETAIL_URL
)


class UnauthenticatedUserTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_unauthenticated_user(self):
        response = self.client.get(BASE_URL)
        response_detail = self.client.get(DETAIL_URL)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response_detail.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedUserTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="test-1-2-3",
        )
        self.client.force_authenticate(self.user)

    def test_authenticated_user(self):
        response = self.client.get(BASE_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
