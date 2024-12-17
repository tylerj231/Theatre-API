from django.db.models import Count, F
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets

from core.models import (
    TheatreHall,
    Play,
    Performance,
    Actor,
    Genre,
    Ticket,
    Reservation
)

from core.serializers import (
    TheatreHallSerializer,
    PerformanceSerializer,
    PlaySerializer,
    ActorSerializer,
    GenreSerializer,
    TicketSerializer,
    ReservationSerializer,
    TicketListSerializer,
    ReservationListSerializer,
    PerformanceListSerializer,
    PlayListSerializer,
    ActorListSerializer,
    PlayRetrieveSerializer,
    TheatreHallRetrieveSerializer,
    TicketRetrieveSerializer,
    PerformanceRetrieveSerializer,
    ReservationRetrieveSerializer,
)
from user.permissions import (
    IsAdminOrIfAuthenticatedReadOnly,
    IsAdminOrIfAuthenticatedCreateAndReadAndDelete
)


class PerformanceViewSet(viewsets.ModelViewSet):
    queryset = Performance.objects.all()
    serializer_class = PerformanceSerializer
    permission_classes = [IsAdminOrIfAuthenticatedReadOnly]

    def get_serializer_class(self):
        if self.action == 'list':
            return PerformanceListSerializer
        elif self.action == 'retrieve':
            return PerformanceRetrieveSerializer

        return PerformanceSerializer

    def get_queryset(self):
        queryset = self.queryset

        if self.action == 'list':
            queryset = queryset.prefetch_related(
                "play",
                "theatre_hall",
                "tickets",
            ).annotate(
                available_seats=F("theatre_hall__rows")
                                * F("theatre_hall__seats_in_row")
                                - Count("tickets__reservations")

            )
        play = self.request.query_params.get('play', None)
        date = self.request.query_params.get('date', None)

        if play:
            play_ids = [int(str_id) for str_id in play.split(',')]
            queryset = queryset.filter(play_id__in=play_ids)

        if date:
            queryset = queryset.filter(show_time__date=date)

        return queryset.distinct()

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "play",
                type={"type": "array", "items": {"type": "number"}},
                description="Filter performance by play id, Example:(?play=1,2)",
            ),
            OpenApiParameter(
                "date",
                type={"type":"string"},
                description="Filter performance by date, Example:(?date=2024-12-20)",

            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class PlayViewSet(viewsets.ModelViewSet):
    serializer_class = PlaySerializer
    queryset = Play.objects.all()
    permission_classes = [IsAdminOrIfAuthenticatedReadOnly]

    def get_serializer_class(self):
        if self.action == 'list':
            return PlayListSerializer
        if self.action == 'retrieve':
            return PlayRetrieveSerializer

        return PlaySerializer


class TheatreHallViewSet(viewsets.ModelViewSet):
    queryset = TheatreHall.objects.all()
    serializer_class = TheatreHallSerializer
    permission_classes = [IsAdminOrIfAuthenticatedReadOnly]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return TheatreHallRetrieveSerializer
        return TheatreHallSerializer


class ActorViewSet(viewsets.ModelViewSet):
    queryset = Actor.objects.prefetch_related("plays")
    serializer_class = ActorSerializer
    permission_classes = [IsAdminOrIfAuthenticatedReadOnly]

    def get_serializer_class(self):
        if self.action == 'list':
            return ActorListSerializer
        return ActorSerializer


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrIfAuthenticatedReadOnly]


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [IsAdminOrIfAuthenticatedReadOnly]

    def get_serializer_class(self):
        if self.action == 'list':
            return TicketListSerializer
        if self.action == 'retrieve':
            return TicketRetrieveSerializer

        return TicketSerializer

    def get_queryset(self):
        queryset = Ticket.objects.prefetch_related("reservations", "performance")
        queryset = queryset.exclude(reservations__isnull=False)

        return queryset.distinct()


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all().select_related("ticket")
    serializer_class = ReservationSerializer
    permission_classes = [IsAdminOrIfAuthenticatedCreateAndReadAndDelete]

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user, ticket__isnull=False)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return ReservationListSerializer
        elif self.action == 'retrieve':
            return ReservationRetrieveSerializer

        return ReservationSerializer
