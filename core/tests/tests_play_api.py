from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from core.models import Play, Actor, Genre
from core.serializers import PlayListSerializer, PlayRetrieveSerializer
from core.config_for_tests import create_sample_plays

BASE_URL = reverse("core:play-list")
DETAIL_URL = reverse("core:play-detail", kwargs={"pk": 1})


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

    def test_play_list(self):
        create_sample_plays()
        response = self.client.get(BASE_URL)

        plays = Play.objects.all()
        serializer = PlayListSerializer(plays, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_play_retrieve(self):
        play_with_genre_and_actor = create_sample_plays()

        actor = Actor.objects.create(
            first_name="Sponge",
            last_name="Bob",
        )
        genre = Genre.objects.create(
            name="Sci-Fi",
        )

        play_with_genre_and_actor.genres.add(genre)
        play_with_genre_and_actor.actors.add(actor)

        response = self.client.get(DETAIL_URL)

        play = Play.objects.get(pk=play_with_genre_and_actor.pk)

        serializer = PlayRetrieveSerializer(play, many=False)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_play_create_forbidden(self):
        payload = {
            "title": "test play",
            "description": "test play",
        }
        response = self.client.post(BASE_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_play_delete_forbidden(self):
        play = create_sample_plays()
        url = reverse("core:play-detail", kwargs={"pk": play.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_play_create_allow(self):
        self.user.is_staff = True
        payload = {
            "title": "test play",
            "description": "test play",
        }
        url = reverse("core:play-list")
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_admin_play_delete_allow(self):
        self.user.is_staff = True
        play = create_sample_plays()
        url = reverse("core:play-detail", kwargs={"pk": play.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
