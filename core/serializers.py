from argparse import Action

from django.db import transaction
from rest_framework import serializers

from core.models import Play, Actor, Genre, Performance, TheatreHall, Ticket, Reservation


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
            "actor",
        )
class ActorListSerializer(serializers.ModelSerializer):
    plays = serializers.SlugRelatedField(many=True, read_only=True, slug_field="title")
    class Meta:
        model = Actor
        fields = ("id", "actor", "plays",)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ("name",)

class PlayListSerializer(PlaySerializer):
    actors = ActorSerializer(many=True, read_only=True)
    genres = GenreSerializer(many=True, read_only=True)

    class Meta:
        model = Play
        fields = PlaySerializer.Meta.fields + ("actors", "genres")


class PerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Performance
        fields = (
            "id",
            "play",
            "show_time",
            "theatre_hall"
        )

class TheatreHallSerializer(serializers.ModelSerializer):
    class Meta:
        model = TheatreHall
        fields = (
            "id",
            "name",
        )

class PerformanceListSerializer(PerformanceSerializer):
    theatre_hall = serializers.CharField(source="theatre_hall.name")
    play = serializers.CharField(source="play.title", read_only=True)
    class Meta:
        model = Performance
        fields = PerformanceSerializer.Meta.fields + ("play",)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = (
            "id",
            "name",
        )


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = (
            "id",
            "row",
            "seat",
        )


class TicketListSerializer(TicketSerializer):
    class Meta:
        model = Ticket
        fields = TicketSerializer.Meta.fields + ("performance", "reservation")


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = (
            "id",
            "created_at",
            "tickets",
        )

    def create(self, validated_data):
        with transaction.atomic():
            tickets_data = validated_data.pop("tickets")
            reservation = Reservation.objects.create(**validated_data)
            for ticket_data in tickets_data:
                Ticket.objects.create(reservation=reservation, **ticket_data)
            return reservation


class ReservationListSerializer(ReservationSerializer):
    tickets = TicketListSerializer(many=True, read_only=False)

    class Meta:
        model = Reservation
        fields = ReservationSerializer.Meta.fields
