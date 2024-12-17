from datetime import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from core.models import (
    Play,
    Performance,
    TheatreHall,
)

BASE_URL = reverse("core:play-list")
DETAIL_URL = reverse("core:play-detail", kwargs={"pk": 1})


def create_sample_plays(**kwargs) -> Play:
    defaults = {
        "title": "Test Play",
        "description": "Test Play",
    }
    defaults.update(kwargs)
    return Play.objects.create(**defaults)


def create_sample_theatre(**kwargs) -> TheatreHall:
    defaults = {"name": "Test Theatre", }
    defaults.update(kwargs)
    return TheatreHall.objects.create(**defaults)


def create_sample_performance(**kwargs) -> Performance:
    defaults = {
        "play": create_sample_plays(),
        "show_time": datetime.now(),
        "theatre_hall": create_sample_theatre(),
    }
    defaults.update(kwargs)
    return Performance.objects.create(**defaults)


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
