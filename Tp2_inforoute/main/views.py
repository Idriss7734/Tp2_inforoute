from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.authentication import SessionAuthentication, TokenAuthentication, BasicAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.parsers import JSONParser 
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

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
    return Response(status=status.HTTP_200_OK)

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
    method="delete", tags=["Settings"], 
    manual_parameters=[
    openapi.Parameter('username',in_=openapi.IN_QUERY, description='username', type=openapi.TYPE_STRING), 
    ]
)
@swagger_auto_schema(
    method="put", tags=["Settings"], 
    request_body=SettingsAccountSerializer,
    manual_parameters=[
        openapi.Parameter('id',in_=openapi.IN_QUERY, description='id', type=openapi.TYPE_INTEGER), 
        openapi.Parameter('username',in_=openapi.IN_QUERY, description='username', type=openapi.TYPE_STRING), 
        openapi.Parameter('old_password',in_=openapi.IN_QUERY, description='old_password', type=openapi.TYPE_STRING),
        openapi.Parameter('new_password',in_=openapi.IN_QUERY, description='new_password', type=openapi.TYPE_STRING),
        openapi.Parameter('birthday',in_=openapi.IN_QUERY, description='birthday', type=openapi.TYPE_STRING),
        ]
)
@swagger_auto_schema(
    method="post", tags=["Settings"], request_body=SettingsAccountSerializer,

)
@api_view(["POST", "GET", "PUT", "DELETE"])
@permission_classes([IsAuthenticated])
@authentication_classes((SessionAuthentication, TokenAuthentication, BasicAuthentication))
def settings(request):
    
    admin = True
    token_key = request.META["HTTP_AUTHORIZATION"].split(" ")[1]
    print(token_key)
    user = Token.objects.filter(key="a23af3eff3a14f3610a2d28d8d2dd34f8e9c57e7").first()
    #CustomUser = CustomUser.objects.filter(key="a23af3eff3a14f3610a2d28d8d2dd34f8e9c57e7").exists()
    print(user)
    #CustomUser = CustomUser.objects.get(username=username)

    #if not CustomUser.objects.filter(auth_token=token_key).exists():
    #    return Response(
    #        {"message": "L'utilisateur n'existe pas !"},
    #        status=status.HTTP_404_NOT_FOUND,
    #    )
    if request.method == "GET":
        if admin:
            SettingsAccount = CustomUser.objects.all()
            SettingsAccount_serializer = SettingsAccountSerializer(SettingsAccount, many=True)
            return Response(
                SettingsAccount_serializer.data,
                status=status.HTTP_200_OK,
            )
        else:
            SettingsAccount = CustomUser.objects.get(auth_token=user)
            SettingsAccount_serializer = SettingsAccountSerializer(SettingsAccount)
            return Response(
                SettingsAccount_serializer.data,
                status=status.HTTP_200_OK,
            )
    elif request.method == "PUT":
        if admin:
            try:
                SettingsAccounts = CustomUser.objects.all()
                id = request.GET.get('id')
                username = request.GET.get('username')
                old_password = request.GET.get('old_password')
                new_password = request.GET.get('new_password')
                birthday = request.GET.get('birthday')

                for user in SettingsAccounts:
                    if user.id == int(id):
                        account = user

                data = {'username':account.username, 'password':account.password, 'birthday': account.birthday}
                if username != None:
                    data['username'] = username

                if old_password != None and  check_password(old_password, account.password):
                    password=make_password(new_password)
                    data['password'] = password

                if birthday != None:
                    data['birthday'] = birthday

                SettingsAccount_serializer = SettingsAccountSerializer(account,data=data)
                if not SettingsAccount_serializer.is_valid():
                    return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                SettingsAccount_serializer.save()
                return Response(status=status.HTTP_200_OK)
            except:
                return Response("The user id is invalide.",status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            SettingsAccounts = CustomUser.objects.get(auth_token=user)
            username = request.GET.get('username')
            old_password = request.GET.get('old_password')
            new_password = request.GET.get('new_password')
            birthday = request.GET.get('birthday')
            
            data = {'username':SettingsAccounts.username, 'password':SettingsAccounts.password, 'birthday': SettingsAccounts.birthday}

            if username != None:
                data['username'] = username

            if old_password != None and  check_password(old_password, SettingsAccounts.password):
                password=make_password(new_password)
                data['password'] = password

            if birthday != None:
                data['birthday'] = birthday


            SettingsAccount_serializer = SettingsAccountSerializer(SettingsAccounts,data=data)
            if not SettingsAccount_serializer.is_valid():
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            SettingsAccount_serializer.save()
            return Response(status=status.HTTP_200_OK)
    elif request.method == "DELETE":
        if admin:
            username = request.GET.get('username')
            student = get_object_or_404(CustomUser, username=username)
            
            #user = CustomUser.objects.filter(username=username)
            #student_data = CustomUser.objects.get(username=username).delete()
            print(student)
            student.delete()
   

            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    
    

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
        
