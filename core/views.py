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


class PerformanceViewSet(viewsets.ModelViewSet):
    queryset = Performance.objects.all()
    serializer_class = PerformanceSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return PerformanceListSerializer
        elif self.action == 'retrieve':
            return PerformanceRetrieveSerializer

        return PerformanceSerializer

    def get_queryset(self):
        queryset = self.queryset

        play =  self.request.query_params.get('play', None)

        if play:
            play_ids = [int(str_id) for str_id in play.split(',')]
            queryset = queryset.filter(play_id__in=play_ids)

        return queryset.distinct()

class PlayViewSet(viewsets.ModelViewSet):
    serializer_class = PlaySerializer
    queryset = Play.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return PlayListSerializer
        if self.action == 'retrieve':
            return PlayRetrieveSerializer

        return PlaySerializer

class TheatreHallViewSet(viewsets.ModelViewSet):
    queryset = TheatreHall.objects.all()
    serializer_class = TheatreHallSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return TheatreHallSerializer
        if self.action == 'retrieve':
            return TheatreHallRetrieveSerializer
        return TheatreHallSerializer


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
        if self.action == 'retrieve':
            return TicketRetrieveSerializer

        return TicketSerializer


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all().select_related("tickets")
    serializer_class = ReservationSerializer

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return ReservationListSerializer
        elif self.action == 'retrieve':
            return ReservationRetrieveSerializer

        return ReservationSerializer
