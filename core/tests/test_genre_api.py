from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from core.models import Genre
from core.serializers import GenreSerializer


class AuthenticatedUserTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="test-1-2-3",
        )
        self.client.force_authenticate(self.user)

    def test_genre_list(self):
        Genre.objects.create(
            name="Test Genre",
        )
        url = reverse("core:genre-list")
        response = self.client.get(url)
        genres = Genre.objects.all()
        serializer = GenreSerializer(genres, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_genre_create_forbidden(self):
        payload = {
            "name": "test genre",
        }
        url = reverse("core:genre-list")
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_genre_delete_forbidden(self):
       genre = Genre.objects.create(
           name="Test Genre",
       )
       url = reverse("core:genre-detail", kwargs={"pk": genre.id})
       response = self.client.delete(url)
       self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_create_genre_allow(self):
        self.user.is_staff = True
        self.user.save()
        payload = {
            "name": "test genre",
        }

        url = reverse("core:genre-list")
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_admin_delete_genre_allow(self):
        self.user.is_staff = True
        self.user.save()
        genre = Genre.objects.create(
            name="Test Genre",
        )
        url = reverse("core:genre-detail", kwargs={"pk": genre.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
