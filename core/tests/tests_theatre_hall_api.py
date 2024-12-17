from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from core.models import TheatreHall
from core.serializers import TheatreHallSerializer, TheatreHallRetrieveSerializer


class AuthenticatedUserTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="test-1-2-3",
        )
        self.client.force_authenticate(self.user)

    def test_theater_hall_list(self):
        TheatreHall.objects.create(
            name="Test Theatre Hall",
        )

        url = reverse("core:theatrehall-list")

        response = self.client.get(url)

        theatre_halls = TheatreHall.objects.all()

        serializer = TheatreHallSerializer(theatre_halls, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_theatre_hall_detail(self):
        TheatreHall.objects.create(
            name="Test Theatre Hall",
        )

        url = reverse(
            "core:theatrehall-detail",
            kwargs={"pk": 1}
        )

        response = self.client.get(url)

        theatre_hall = TheatreHall.objects.get(pk=response.data["id"])
        serializer = TheatreHallRetrieveSerializer(theatre_hall)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_theatre_hall_create_forbidden(self):
        payload = {
            "name": "Hall # 1",
        }
        url = reverse("core:theatrehall-list")
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_theatre_hall_delete_forbidden(self):
        theatre_hall =  TheatreHall.objects.create(
            name="Test Theatre Hall",
        )
        url = reverse("core:theatrehall-detail", kwargs={"pk": theatre_hall.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_theatre_hall_create_allow(self):
        self.user.is_staff = True
        payload = {
            "name": "Test Theatre Hall",
        }
        url = reverse("core:theatrehall-list")
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_admin_theatre_hall_delete_allow(self):
        self.user.is_staff = True
        theatre_hall = TheatreHall.objects.create(
            name="Test Theatre Hall",
        )
        url = reverse("core:theatrehall-detail", kwargs={"pk": theatre_hall.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
