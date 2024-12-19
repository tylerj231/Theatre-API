from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from core.models import Ticket
from core.serializers import (
    TicketListSerializer,
    TicketRetrieveSerializer
)
from core.tests.config_for_tests import create_sample_performance


class AuthenticatedUserTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="test-1-2-3",
        )
        self.client.force_authenticate(self.user)

    def test_ticket_list(self):
        Ticket.objects.create(
            row=1,
            seat=1,
            performance=create_sample_performance(),
        )

        url = reverse("core:ticket-list")

        response = self.client.get(url)

        tickets = Ticket.objects.all()

        serializer = TicketListSerializer(tickets, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_ticket_detail(self):
        ticket = Ticket.objects.create(
            row=1,
            seat=1,
            performance=create_sample_performance(),
        )
        url = reverse("core:ticket-detail", args=[ticket.id])

        response = self.client.get(url)

        serializer = TicketRetrieveSerializer(ticket)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_ticket_create_forbidden(self):
        payload = {
            "row": 10,
            "seat": 5,
        }
        url = reverse("core:ticket-list")
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_play_delete_forbidden(self):
        ticket = Ticket.objects.create(
            row=1,
            seat=1,
        )
        url = reverse("core:ticket-detail", kwargs={"pk": ticket.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_create_ticket_allow(self):
        performance = create_sample_performance()
        self.user.is_staff = True
        payload = {
            "row": 1,
            "seat": 1,
            "performance": performance.id,
        }
        url = reverse("core:ticket-list")
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_admin_delete_ticket_allow(self):
        self.user.is_staff = True
        performance = create_sample_performance()
        ticket = Ticket.objects.create(
            row=1,
            seat=1,
            performance=performance,
        )
        url = reverse("core:ticket-detail", kwargs={"pk": ticket.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
