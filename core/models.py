from django.contrib.auth.models import AbstractUser
from django.db import models
from rest_framework.exceptions import ValidationError

from theatre_service import settings


class Actor(models.Model):
    first_name = models.CharField(max_length=75, unique=True)
    last_name = models.CharField(max_length=75, unique=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Play(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    actors = models.ManyToManyField(
        Actor,
        related_name="plays",
    )
    genres = models.ManyToManyField(
        Genre,
        related_name="plays",
    )

    def __str__(self):
        return self.title

class TheatreHall(models.Model):
    name = models.CharField(max_length=100)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()

    def __str__(self):
        return self.name


class Performance(models.Model):
    play = models.ForeignKey(
        Play,
        on_delete=models.CASCADE,
        related_name='performances')

    theatre_hall = models.ForeignKey(
        TheatreHall,
        on_delete=models.CASCADE,
        related_name='performances'
    )
    show_time = models.DateTimeField()

    def __str__(self):
        return f"{self.theatre_hall.name} - {self.play.title}"

class Reservation(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user =  models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reservations'
    )

    def __str__(self):
        return f"Reservation for {self.user.username}"

class Ticket(models.Model):
    row = models.IntegerField()
    seat = models.IntegerField()

    performance = models.ForeignKey(
        Performance,
        on_delete=models.CASCADE,
        related_name='tickets',
        null=True,
        blank=True,
    )
    reservation = models.ForeignKey(
        Reservation,
        on_delete=models.CASCADE,
        related_name='tickets',
        null=True,
        blank=True,

    )

    class Meta:
        unique_together = ('row', 'seat')

    @staticmethod
    def validate_seat_and_row(seat: int, seats_in_row: int, row: int, rows: int, error_to_raise,):
        if not (1 <= seat <= seats_in_row):
            raise error_to_raise({
                "seat": f"seat must be in the range [1, {seats_in_row}]"
            })
        elif not (1 <= row <= rows):
            raise error_to_raise({
                "row": f"row must be in the range [1, {rows}]"
            })

    def clean(self):
        Ticket.validate_seat_and_row(
            self.seat,
            self.performance.theatre_hall.seats_in_row,
            self.row,
            self.performance.theatre_hall.rows,
            ValidationError
        )



class User(AbstractUser):
    pass