from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from core.models import Actor
from core.serializers import ActorListSerializer, ActorSerializer
from core.config_for_tests import create_sample_plays


class AuthenticatedUserTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="test-1-2-3",
        )
        self.client.force_authenticate(self.user)

    def test_actor_list(self):
        actor_1 = Actor.objects.create(
            first_name="Jason",
            last_name="Statham",
        )

        actor_1.plays.add(create_sample_plays())

        url = reverse("core:actor-list")
        response = self.client.get(url)
        actors = Actor.objects.all()
        serializer = ActorListSerializer(actors, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_actor_retrieve(self):
        actor = Actor.objects.create(
            first_name="Jason",
            last_name="Statham",
        )

        url = reverse("core:actor-detail", args=[actor.id])
        response = self.client.get(url)

        serializer = ActorSerializer(actor)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_actor_create_forbidden(self):
        payload = {
            "first_name": "test name",
            "last_name": "test last name",
        }
        url = reverse("core:actor-list")
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_play_delete_forbidden(self):
        actor = Actor.objects.create(
            first_name="Jason",
            last_name="Statham",
        )
        url = reverse("core:actor-detail", kwargs={"pk": actor.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_actor_create_allow(self):
        self.user.is_staff = True
        payload = {
            "first_name": "Jason",
            "last_name": "Statham",
        }
        url = reverse("core:actor-list")
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_admin_delete_allow(self):
        self.user.is_staff = True
        actor = Actor.objects.create(
            first_name="Jason",
            last_name="Statham",
        )
        url = reverse("core:actor-detail", kwargs={"pk": actor.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
