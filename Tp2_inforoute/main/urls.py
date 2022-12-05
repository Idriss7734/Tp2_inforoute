from django.urls import path, include
from rest_framework import routers

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from .views import register, login, settings, logout, getTexts, getQuizs, addTts, getTextAndQuiz, postAttempt, viewResult, addText, addPhrase, addQuiz, getPhrases, modifyText, modifyPhrase, modifyQuiz, deleteText, deletePhrase, deleteQuiz

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
    path("addText/", addText, name='addText'),
    path("addPhrase/", addPhrase, name='addPhrase'),
    path("addQuiz/", addQuiz, name='addQuiz'), 
    path("getTexts/", getTexts, name='getTexts'),
    path("modifyText/", modifyText, name='modifyText'),
    path("deleteText/", deleteText, name='deleteText'),
    path("getPhrases/", getPhrases, name='getPhrases'), 
    path("modifyPhrase/", modifyPhrase, name='modifyPhrase'),
    path("deletePhrase/", deletePhrase, name='deletePhrase'),
    path("getQuizs/", getQuizs, name='getQuizs'),
    path("modifyQuiz/", modifyQuiz, name='modifyQuiz'),
    path("deleteQuiz/", deleteQuiz, name='deleteQuiz'),
    path("addTts/", addTts, name="addTts"),
    path("Get Text and Quizs with a title/", getTextAndQuiz, name="Get text and quizs"),
    path("Post Attempt/", postAttempt, name="postAttempt"),
    path("viewResult/", viewResult, name="viewResult"),
    path(
        "swagger",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
]