from datetime import datetime

from django.urls import reverse

from core.models import Play, TheatreHall, Performance


BASE_URL = reverse("core:play-list")
DETAIL_URL = reverse("core:play-detail", kwargs={"pk": 1})


def create_sample_plays(**kwargs) -> Play:
    defaults = {
        "title": "Test Play",
        "description": "Test Play",
    }
    defaults.update(kwargs)
    return Play.objects.create(**defaults)


def create_sample_theatre(**kwargs) -> TheatreHall:
    defaults = {
        "name": "Test Theatre",
    }
    defaults.update(kwargs)
    return TheatreHall.objects.create(**defaults)


def create_sample_performance(**kwargs) -> Performance:
    defaults = {
        "play": create_sample_plays(),
        "show_time": datetime.now(),
        "theatre_hall": create_sample_theatre(),
    }
    defaults.update(kwargs)
    return Performance.objects.create(**defaults)
