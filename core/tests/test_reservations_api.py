from datetime import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from core.models import Ticket, Reservation
from core.serializers import ReservationListSerializer


class AuthenticatedUserTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="test-1-2-3",
        )
        self.client.force_authenticate(self.user)

    def test_reservations_list(self):
        ticket = Ticket.objects.create(
            row=1,
            seat=1,
        )

        Reservation.objects.create(
            created_at=datetime.now(),
            ticket=ticket,
            user_id=self.user.id,
        )

        url = reverse("core:reservation-list")

        response = self.client.get(url)

        reservations = Reservation.objects.all()

        serializer = ReservationListSerializer(reservations, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_reservation_allow_create(self):
        ticket = Ticket.objects.create(
            row=1,
            seat=1,
        )
        payload = {
            "ticket": ticket.id,
        }
        url = reverse("core:reservation-list")
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_reservation_allow_delete(self):
        ticket = Ticket.objects.create(
            row=1,
            seat=1,
        )
        reservation = Reservation.objects.create(
            created_at=datetime.now(),
            ticket=ticket,
            user_id=self.user.id,
        )
        url = reverse("core:reservation-detail", args=[reservation.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_admin_reservation_allow_create(self):
        self.user.is_staff = True
        ticket = Ticket.objects.create(
            row=1,
            seat=1,
        )

        payload = {
            "ticket": ticket.id,
        }
        url = reverse("core:reservation-list")
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_admin_reservation_allow_delete(self):
        self.user.is_staff = True
        ticket = Ticket.objects.create(
            row=1,
            seat=1,

        )
        reservation = Reservation.objects.create(
            created_at=datetime.now(),
            ticket=ticket,
            user_id=self.user.id,
        )
        url = reverse("core:reservation-detail", args=[reservation.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
