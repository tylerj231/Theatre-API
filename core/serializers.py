from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from core.models import (
    Play,
    Actor,
    Genre,
    Performance,
    TheatreHall,
    Ticket,
    Reservation,
)


class PlaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Play
        fields = (
            "id",
            "title",
            "description",
        )


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = (
            "id",
            "first_name",
            "last_name",
        )


class ActorListSerializer(ActorSerializer):
    plays = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="title",
    )

    class Meta:
        model = Actor
        fields = ActorSerializer.Meta.fields + ("plays",)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ("name",)


class PlayListSerializer(PlaySerializer):
    class Meta:
        model = Play
        fields = PlaySerializer.Meta.fields


class PerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Performance
        fields = (
            "id",
            "play",
            "show_time",
            "theatre_hall",
        )


class PerformanceListSerializer(PerformanceSerializer):
    theatre_hall = serializers.CharField(
        source="theatre_hall.name"
    )

    play = serializers.CharField(
        source="play.title",
        read_only=True
    )
    available_seats = serializers.IntegerField(
        read_only=True,
    )

    class Meta:
        model = Performance
        fields = PerformanceSerializer.Meta.fields + ("play", "available_seats")


class PlayRetrieveSerializer(PlaySerializer):
    actors = serializers.StringRelatedField(
        many=True,
        read_only=True,
    )
    genres = serializers.StringRelatedField(
        many=True,
        read_only=True,
    )
    performances = PerformanceListSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = Play
        fields = PlaySerializer.Meta.fields + (
            "actors",
            "genres",
            "performances",
        )


class TheatreHallSerializer(serializers.ModelSerializer):
    class Meta:
        model = TheatreHall
        fields = (
            "id",
            "name",
        )


class TheatreHallRetrieveSerializer(TheatreHallSerializer):
    class Meta:
        model = TheatreHall
        fields = TheatreHallSerializer.Meta.fields + ("rows", "seats_in_row")


class PerformanceRetrieveSerializer(PerformanceSerializer):
    theatre_hall = TheatreHallRetrieveSerializer(read_only=True)
    play = serializers.CharField(
        source="play.title",
        read_only=True
    )


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = (
            "id",
            "row",
            "seat",
            "performance",
        )

    def validate(self, attrs):
        data = super(TicketSerializer, self).validate(attrs)
        Ticket.validate_seat_and_row(
            attrs["seat"],
            attrs["performance"].theatre_hall.seats_in_row,
            attrs["row"],
            attrs["performance"].theatre_hall.rows,
            serializers.ValidationError,
        )
        return data


class TicketListSerializer(TicketSerializer):
    performance = serializers.SlugRelatedField(
        slug_field="play.title",
        read_only=True
    )

    class Meta:
        model = Ticket
        fields = TicketSerializer.Meta.fields


class TicketRetrieveSerializer(TicketSerializer):
    performance = PerformanceListSerializer()


class ReservationSerializer(serializers.ModelSerializer):
    ticket = serializers.PrimaryKeyRelatedField(
        queryset=Ticket.objects.filter(reservations__isnull=True),
        label="Available Tickets",
    )

    class Meta:
        model = Reservation
        fields = (
            "id",
            "created_at",
            "ticket",
        )
        validators = [
            UniqueTogetherValidator(
                queryset=Reservation.objects.all().select_related("ticket"),
                fields=("ticket",),
                message="The reservation for this ticket already exists.",
            )
        ]


class ReservationListSerializer(ReservationSerializer):
    pass


class ReservationRetrieveSerializer(ReservationSerializer):
    pass
