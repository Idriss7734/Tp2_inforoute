from django.urls import path, include
from rest_framework import routers

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from .views import register, login

schema_view = get_schema_view(
    openapi.Info(
        title="Tp2",
        default_version="v1.0",
        description="Application pour les gens qui ont de la difficulté à lire.",
    ),
    public=True,
)

urlpatterns = [
    path("", login, name="login"),
    path("", register, name="register"),
    path(
        "swagger",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
]