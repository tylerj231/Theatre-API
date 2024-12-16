from django.contrib import admin

from core.models import (
    Performance,
    Play,
    Ticket,
    TheatreHall,
    Reservation,
    Actor,
    Genre,
)

admin.site.register(Performance)
admin.site.register(Play)
admin.site.register(Ticket)
admin.site.register(TheatreHall)
admin.site.register(Actor)
admin.site.register(Genre)
admin.site.register(Reservation)
