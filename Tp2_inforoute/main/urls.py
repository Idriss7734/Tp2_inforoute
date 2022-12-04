from django.urls import path, include
from rest_framework import routers

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from .views import register, login, settings, logout, text, quiz, addText, getTextAndQuiz, postAttempt, viewResult

schema_view = get_schema_view(
    openapi.Info(
        title="Tp2",
        default_version="v1.0",
        description="Application pour les gens qui ont de la difficulté à lire.",
    ),
    public=True,
)

urlpatterns = [
    path("Register/", register, name="register"),
    path("Login/", login, name="login"),
    path("Logout/", logout, name="logout"),
    path("Settings/", settings, name='settings'),
    path("Text/", text, name='text'), 
    path("Quiz/", quiz, name='quiz'),
    path("addText/", addText, name="addText"),
    path("Get Text and Quizs with a title/", getTextAndQuiz, name="Get text and quizs"),
    path("Post Attempt/", postAttempt, name="postAttempt"),
    path("viewResult/", viewResult, name="viewResult"),
    path(
        "swagger",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
]