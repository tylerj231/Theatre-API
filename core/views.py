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
        queryset = self.queryset.select_related("play", "theatre_hall")

        if self.action == 'list':
            play = self.request.query_params.get('play', None)
            date = self.request.query_params.get('date', None)

            if play:
                play_ids = [int(str_id) for str_id in play.split(',')]
                queryset = queryset.filter(play_id__in=play_ids)

            if date:
                queryset = queryset.filter(show_time__date=date)

        return queryset.distinct()


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
    queryset = Actor.objects.all()
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
    queryset = Ticket.objects.prefetch_related(
        "performance",
        "reservations"
    )
    serializer_class = TicketSerializer
    permission_classes = [IsAdminOrIfAuthenticatedReadOnly]

    def get_serializer_class(self):
        if self.action == 'list':
            return TicketListSerializer
        if self.action == 'retrieve':
            return TicketRetrieveSerializer

        return TicketSerializer

    def get_queryset(self):
        queryset = Ticket.objects.exclude(reservations__isnull=False)

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
