from django.contrib import admin

from core.models import (
    Performance,
    Play,
    Ticket,
    TheatreHall,
    Reservation,
    Actor,
    Genre
)

admin.site.register(Performance)
admin.site.register(Play)
admin.site.register(Ticket)
admin.site.register(TheatreHall)
admin.site.register(Actor)
admin.site.register(Genre)

class TicketInline(admin.TabularInline):
    model = Ticket

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    inlines = [TicketInline]