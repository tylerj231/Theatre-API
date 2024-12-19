from datetime import datetime

from django.contrib.auth import get_user_model
from django.db.models import F, Count
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from core.models import Performance
from core.serializers import (
    PerformanceListSerializer,
    PerformanceRetrieveSerializer
)
from core.tests.config_for_tests import (
    create_sample_plays,
    create_sample_theatre,
    create_sample_performance
)


class AuthenticatedUserTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="test-1-2-3",
        )
        self.client.force_authenticate(self.user)

    def test_performance_list(self):
        create_sample_performance()
        url = reverse("core:performance-list")
        response = self.client.get(url)
        performances = Performance.objects.prefetch_related(
            "play",
            "theatre_hall",
            "tickets",
        ).annotate(
            available_seats=F("theatre_hall__rows") * F("theatre_hall__seats_in_row")
                            - Count("tickets__reservations")
        )
        serializer = PerformanceListSerializer(performances, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_performance_detail(self):
        performance = create_sample_performance()
        url = reverse("core:performance-detail", args=[performance.id])
        response = self.client.get(url)
        serializer = PerformanceRetrieveSerializer(performance)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_performance_create_forbidden(self):
        play = create_sample_plays()
        theatre = create_sample_theatre()
        payload = {
            "play": play.id,
            "theatre_hall": theatre.id,
            "show_time": datetime.now(),
        }
        url = reverse("core:performance-list")
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_performance_delete_forbidden(self):
        performance = create_sample_performance()
        url = reverse("core:performance-detail", kwargs={"pk": performance.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_performance_allow_create(self):
        self.user.is_staff = True
        play = create_sample_plays()
        theatre_hall = create_sample_theatre()

        payload = {
            "play": play.id,
            "theatre_hall": theatre_hall.id,
            "show_time": datetime.now(),
        }
        url = reverse("core:performance-list")
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_admin_performance_delete(self):
        self.user.is_staff = True
        performance = create_sample_performance()
        url = reverse("core:performance-detail", kwargs={"pk": performance.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
