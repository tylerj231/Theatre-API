from django.shortcuts import render
from rest_framework import viewsets

from core.models import TheatreHall, Play, Performance, Actor, Genre, Ticket, Reservation

from core.serializers import (
    TheatreHallSerializer,
    PerformanceSerializer,
    PlaySerializer,
    ActorSerializer,
    GenreSerializer, TicketSerializer, ReservationSerializer, TicketListSerializer, ReservationListSerializer,
    PerformanceListSerializer, PlayListSerializer, ActorListSerializer,

)


class PerformanceViewSet(viewsets.ModelViewSet):
    queryset = Performance.objects.all()
    serializer_class = PerformanceSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return PerformanceListSerializer

        return PerformanceSerializer


class PlayViewSet(viewsets.ModelViewSet):
    queryset = Play.objects.all()
    serializer_class = PlaySerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return PlayListSerializer

        return PlaySerializer


class TheatreHallViewSet(viewsets.ModelViewSet):
    queryset = TheatreHall.objects.all()
    serializer_class = TheatreHallSerializer

class ActorViewSet(viewsets.ModelViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return ActorListSerializer
        return ActorSerializer

class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return TicketListSerializer

        return TicketSerializer

class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return ReservationListSerializer

        return ReservationSerializer
