from django.urls import include, path
from rest_framework import routers

from core.views import (
    PlayViewSet,
    TheatreHallViewSet,
    TicketViewSet,
    ReservationViewSet,
    ActorViewSet,
    GenreViewSet,
    PerformanceViewSet,
)

app_name = "core"

router = routers.DefaultRouter()
router.register("plays", PlayViewSet)
router.register("theatre-halls", TheatreHallViewSet)
router.register("tickets", TicketViewSet)
router.register("reservations", ReservationViewSet)
router.register("actors", ActorViewSet)
router.register("genres", GenreViewSet)
router.register("performances", PerformanceViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
