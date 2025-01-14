from django.contrib import admin
from django.urls import path, include
from debug_toolbar.toolbar import debug_toolbar_urls
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

urlpatterns = [
    path("admin/",
         admin.site.urls
         ),
    path("theatre/api/",
         include("core.urls",
                 namespace="core"
                 )
         ),

    path("api/user/",
         include("user.urls",
                 namespace="user"
                 )
         ),
    path("api/doc/",
         SpectacularAPIView.as_view(),
         name="schema"
         ),

    path(
        "api/doc/swagger/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/doc/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc"
    ),
] + debug_toolbar_urls()
