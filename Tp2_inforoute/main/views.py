from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.authentication import SessionAuthentication, TokenAuthentication, BasicAuthentication

from drf_yasg.utils import swagger_auto_schema
from gtts import gTTS

from .models import CustomUser, Texts, TextTts, Quizs, Quizattempt
from .serializers import LoginSerializer, RegisterSerializer, SettingsAccountSerializer, TextsSerializer, QuizsSerializer, AddtextSerializer, QuizattemptSerializer


@swagger_auto_schema(
    method="post", tags=["Authentication"], request_body=RegisterSerializer
)
@api_view(["POST", "GET"])
def register(request):
    if request.method == "GET":
        return render(request, "Tp/register.html", {"status": False})
    elif request.method == "POST":
        username = request.data["username"]
        password = request.data["password"]
        birthday = request.data["birthday"]
        is_superuser = request.data["is_superuser"]
        user = CustomUser(username=username, password=make_password(password), birthday=birthday, is_superuser=is_superuser)
        user.save()


@swagger_auto_schema(
    method="post", tags=["Authentication"], request_body=LoginSerializer
)
@api_view(["POST"])
def login(request):
    username = request.data["username"]
    password = request.data["password"]
    
    user = CustomUser.objects.filter(username=username)

    if user.exists():
        auth_success = check_password(password, user.first().password)

        if auth_success:
            token = Token.objects.filter(user=user.first())

            if token.exists():
                return Response(
                    {"token": "Token {}".format(token.first().key)},
                    status=status.HTTP_200_OK,
                )
            else:
                token = Token.objects.create(user=user.first())
                return Response(
                    {"token": "Token {}".format(token.key)}, status=status.HTTP_200_OK
                )
        else:
            return Response(
                {"message": "Mot de passe incorrect !"},
                status=status.HTTP_404_NOT_FOUND,
            )
    else:
        return Response(
            {"message": "L'utilisateur n'existe pas !"},
            status=status.HTTP_404_NOT_FOUND,
        )

@swagger_auto_schema(
    method="post", tags=["Settings"], request_body=SettingsAccountSerializer
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
@authentication_classes((SessionAuthentication, TokenAuthentication, BasicAuthentication))
def settings(request):
    

    token_key = request.META["HTTP_AUTHORIZATION"].split(" ")[1]
    print(token_key)
    CustomUser = Token.objects.filter(key=token_key).first().CustomUser
    
    #CustomUser = CustomUser.objects.filter(key="a23af3eff3a14f3610a2d28d8d2dd34f8e9c57e7").exists()

    #CustomUser = CustomUser.objects.get(username=username)

    if CustomUser.objects.filter(auth_token=token_key).exists():
        return Response(
            {"message": "Utilisateur existe"},
            status=status.HTTP_200_OK,
        )
    else:
        return Response(
            {"message": "L'utilisateur n'existe pas !"},
            status=status.HTTP_404_NOT_FOUND,
        )

@swagger_auto_schema( method="get", tags=["Authentication"])
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def logout(request):
    token_key = request.META["HTTP_AUTHORIZATION"].split(" ")[1]

    invalidated_token = Token.objects.filter(key=token_key).first()
    invalidated_token.delete()

    return Response(
        {"message": "Deconnexion effectuée avec succès !"}, status=status.HTTP_200_OK
    )


@swagger_auto_schema( method="post", tags=["Texts/Quizs"], request_body=TextsSerializer)
@api_view(["POST"])
#@permission_classes([IsAuthenticated])
def text(request):
    textTitle = request.data["title"]
    text = Texts.objects.filter(title=textTitle).first()
    
    return Response(
        {"message": "Phrase: {}".format(text.phrase)}, status=status.HTTP_200_OK
    )

@swagger_auto_schema( method="post", tags=["Texts/Quizs"], request_body=QuizsSerializer)
@api_view(["POST"])
#@permission_classes([IsAuthenticated])
def quiz(request):
    text = request.data["idText"]
    phrase = Quizs.objects.filter(idText=text).first()

    return Response(
        {"message": "Phrase: {}, Reponse1: {}, Reponse2: {}, Reponse3: {}, Reponse4: {}".format(phrase.phrase, phrase.reponse1, phrase.reponse2, phrase.reponse3, phrase.reponse4)}, status=status.HTTP_200_OK
    )

@swagger_auto_schema( method="post", tags=["Texts/Quizs"], request_body=TextsSerializer)
@api_view(["POST"])
#@permission_classes([IsAuthenticated])
def getTextAndQuiz(request):
    textTitle = request.data["title"]

    text = Texts.objects.filter(title = textTitle)
    text_seri = TextsSerializer(text, many=True)
    quizs = Quizs.objects.filter(idText = text[:1]) #text[:1] = premier champ d'un element de type text, ce qui donne l'id
    quiz_seri = QuizsSerializer(quizs, many=True)
  
    return Response(
        {"message": "Texts: {}  Quizs: {}".format(text_seri.data, quiz_seri.data)}, status=status.HTTP_200_OK
    )

@swagger_auto_schema( method="post", tags=["Texts/Quizs"], request_body=QuizattemptSerializer)
@api_view(["POST"])
#@permission_classes([IsAuthenticated])
def postAttempt(request):
    username = request.data["username"]
    quiz = request.data["quiz"]
    reponse = request.data["reponse"]
    attempt = Quizattempt(username=username, quiz=quiz, reponse=reponse)
    attempt.save()

    return Response(
        {"message": "pas d'erreur less gooo"}, status=status.HTTP_200_OK
    )


@swagger_auto_schema(method="post", tags=["Texts/Quizs"], request_body=AddtextSerializer)
@api_view(["POST"])
def addText(request):
    title = request.data["title"]
    audio_file = request.data["text"]
    if request.method == 'POST':
        ttsAdd = TextTts(title:=title, audio_file:=audio_file)
        ttsAdd.savef()
        #ttsAdd.save()
        

