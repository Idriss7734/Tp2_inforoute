from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework import status, viewsets, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.authentication import SessionAuthentication, TokenAuthentication, BasicAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.parsers import JSONParser 
from rest_framework.generics import GenericAPIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import CustomUser, Texts, TextTts, Quizs, Quizattempt, Phrases
from .serializers import LoginSerializer, RegisterSerializer, SettingsAccountSerializer, TextsSerializer, QuizsSerializer, AddTtsSerializer, QuizattemptSerializer, PhrasesSerializer, addTextSerializer, addQuiz, modifyTextSerializer, modifyPhraseSerializer, putPhraseSerializer, modifyQuizSerializer


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
    
    token_key = request.META["HTTP_AUTHORIZATION"].split(" ")[1]
    user = Token.objects.filter(key=token_key).first()
    u = CustomUser.objects.get(username=request.user)
    if request.method == "GET":
        if u.is_superuser:
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
        if u.is_superuser:
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

                if old_password != None and check_password(old_password, account.password) and new_password != None:
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
                return Response("The user id is invalid.",status=status.HTTP_500_INTERNAL_SERVER_ERROR)
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
        if u.is_superuser:
            username = request.GET.get('username')
            student = get_object_or_404(CustomUser, username=username)
            
            if student.username == str(request.user):
                return Response(status=status.HTTP_400_BAD_REQUEST)

            student.delete()
   
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema( method="get", tags=["Texts/Quizs"])
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getTexts(request):
    texts = Texts.objects.all()
    textseri = TextsSerializer(texts, many=True)
    return Response(
        {"message": "{}".format(textseri.data)}, status=status.HTTP_200_OK
    )

@swagger_auto_schema( method="get", tags=["Texts/Quizs"])
@api_view(["GET"])
#@permission_classes([IsAuthenticated])
def getPhrases(request):
    phrases = Phrases.objects.all()
    phraseseri = PhrasesSerializer(phrases, many=True)
    return Response(
        {"message": "{}".format(phraseseri.data)}, status=status.HTTP_200_OK
    )

@swagger_auto_schema( method="get", tags=["Texts/Quizs"])
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getQuizs(request):
    quizs = Quizs.objects.all()
    quizseri = QuizsSerializer(quizs, many=True)
    return Response(
        {"message": "{}".format(quizseri.data)}, status=status.HTTP_200_OK
    )

@swagger_auto_schema( 
    method="get", 
    tags=["Texts/Quizs"], 
    manual_parameters=[
        openapi.Parameter('title',in_=openapi.IN_QUERY, description='title', type=openapi.TYPE_STRING), 
    ]
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getTextAndQuiz(request):
    textTitle = request.GET.get("title")
    text = Texts.objects.filter(title = textTitle)
    text_seri = TextsSerializer(text, many=True)
    phrases = Phrases.objects.filter(idText=text[:1])#text[:1] = premier champ d'un element de type text, ce qui donne l'id
    phrase_seri = PhrasesSerializer(phrases, many=True)
    quizs = Quizs.objects.filter(idText = text[:1]) #text[:1] = premier champ d'un element de type text, ce qui donne l'id
    quiz_seri = QuizsSerializer(quizs, many=True)

    return Response(
        {"message": "-Title: {} -Phrases: {} -Quizs: {}".format(text_seri.data, phrase_seri.data, quiz_seri.data)}, status=status.HTTP_200_OK
    )

@swagger_auto_schema( 
    method="post", 
    tags=["Texts/Quizs"], 
    request_body=addTextSerializer,
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def addText(request):

    
    u = CustomUser.objects.get(username=request.user)
    
    if u.is_superuser:
        textTitle = request.data["title"]
        text = Texts(title=textTitle)
        text.save()
        return Response(
            {"message": "Success"}, status=status.HTTP_200_OK
        )
    
    return Response(
        {"message": "Error: Not admin"}, status=status.HTTP_200_OK
    )

@swagger_auto_schema( 
    method="post", 
    tags=["Texts/Quizs"], 
    request_body=PhrasesSerializer,
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def addPhrase(request):
    u = CustomUser.objects.get(username=request.user)
    
    if u.is_superuser:
        idText = request.data["idText"]
        phraseInput = request.data["phrase"]
        phrase = Phrases(idText=idText, phrase=phraseInput)
        phrase.save()
        return Response(
            {"message": "Success"}, status=status.HTTP_200_OK
        )
    
    return Response(
        {"message": "Error: Not admin"}, status=status.HTTP_200_OK
    )

@swagger_auto_schema( 
    method="post", 
    tags=["Texts/Quizs"], 
    request_body=addQuiz,
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def addQuiz(request):
    u = CustomUser.objects.get(username=request.user)

    if u.is_superuser:
        idText = request.data["idText"]
        question = request.data["question"]
        reponse1 = request.data["reponse1"]
        reponse2 = request.data["reponse2"]
        reponse3 = request.data["reponse3"]
        reponse4 = request.data["reponse4"]

        quiz = Quizs(idText=idText, question=question, reponse1=reponse1, reponse2=reponse2, reponse3=reponse3, reponse4=reponse4)
        quiz.save()
        return Response(
            {"message": "Success"}, status=status.HTTP_200_OK
        )
    
    return Response(
        {"message": "Error: Not admin"}, status=status.HTTP_200_OK
    )

@swagger_auto_schema( 
    method="put", 
    tags=["Texts/Quizs"], 
    request_body=modifyTextSerializer,
    manual_parameters=[
        openapi.Parameter('id',in_=openapi.IN_QUERY, description='id', type=openapi.TYPE_INTEGER),  
        openapi.Parameter('title',in_=openapi.IN_QUERY, description='title', type=openapi.TYPE_STRING),
    ]
)
@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def modifyText(request):
    u = CustomUser.objects.get(username=request.user)
    if u.is_superuser:
        try:
            if request.GET.get('id') == None:
                id = request.data['id']
            else:
                id = request.GET.get('id')

            title = request.GET.get('title')
            texts = Texts.objects.all()

            for t in texts:
                if t.id == int(id):
                    text = t  

            data = {'title': text.title}

            if title != None:
                data['title'] = title

            text_seri = addTextSerializer(text, data=data)
            if not text_seri.is_valid():
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            text_seri.save()
            return Response(status=status.HTTP_200_OK)
        except:
            return Response("The user id is invalid.",status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response("The user not an admin",status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@swagger_auto_schema( method="put", tags=["Texts/Quizs"], request_body=modifyPhraseSerializer,
    manual_parameters=[
        openapi.Parameter('id',in_=openapi.IN_QUERY, description='id', type=openapi.TYPE_INTEGER),  
        openapi.Parameter('phrase',in_=openapi.IN_QUERY, description='phrase', type=openapi.TYPE_STRING),
    ]
)
@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def modifyPhrase(request):
    u = CustomUser.objects.get(username=request.user)
    if u.is_superuser:
        try:
            if request.GET.get('id') == None:
                id = request.data['id']
            else:
                id = request.GET.get('id')

            newPhrase = request.GET.get('phrase')
            phrases = Phrases.objects.all()

            for p in phrases:
                if p.id == int(id):
                    phrase = p  

            data = {'phrase': phrase.phrase}

            if newPhrase != None:
                data['phrase'] = newPhrase

            phrase_seri = putPhraseSerializer(phrase, data=data)
            if not phrase_seri.is_valid():
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            phrase_seri.save()
            return Response(status=status.HTTP_200_OK)
        except:
            return Response("The user id is invalid.",status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response("The user not an admin",status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@swagger_auto_schema( method="put", tags=["Texts/Quizs"], request_body=modifyQuizSerializer,
    manual_parameters=[
        openapi.Parameter('id',in_=openapi.IN_QUERY, description='id', type=openapi.TYPE_INTEGER),  
        openapi.Parameter('question',in_=openapi.IN_QUERY, description='question', type=openapi.TYPE_STRING),
        openapi.Parameter('reponse1',in_=openapi.IN_QUERY, description='reponse1', type=openapi.TYPE_STRING),
        openapi.Parameter('reponse2',in_=openapi.IN_QUERY, description='reponse2', type=openapi.TYPE_STRING),
        openapi.Parameter('reponse3',in_=openapi.IN_QUERY, description='reponse3', type=openapi.TYPE_STRING),
        openapi.Parameter('reponse4',in_=openapi.IN_QUERY, description='reponse4', type=openapi.TYPE_STRING),
    ]
)
@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def modifyQuiz(request):
    u = CustomUser.objects.get(username=request.user)
    if u.is_superuser:
        try:
            if request.GET.get('id') == None:
                id = request.data['id']
            else:
                id = request.GET.get('id') 

            question = request.GET.get('question') 
            reponse1 = request.GET.get('reponse1') 
            reponse2 = request.GET.get('reponse2') 
            reponse3 = request.GET.get('reponse3') 
            reponse4 = request.GET.get('reponse4') 

            quizs = Quizs.objects.all()

            for q in quizs:
                if q.id == int(id):
                    quiz = q  

            data = {'question': quiz.question, 'reponse1': quiz.reponse1, 'reponse2': quiz.reponse2, 'reponse3': quiz.reponse3, 'reponse4': quiz.reponse4}

            if question != None:
                data['question'] = question

            if reponse1 != None:
                data['reponse1'] = reponse1
            
            if reponse2 != None:
                data['reponse2'] = reponse2

            if reponse3 != None:
                data['reponse3'] = reponse3

            if reponse4 != None:
                data['reponse4'] = reponse4

            quiz_seri = QuizsSerializer(quiz, data=data)
            if not quiz_seri.is_valid():
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            quiz_seri.save()
            return Response(status=status.HTTP_200_OK)
        except:
            return Response("The user id is invalid.",status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response("The user not an admin",status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@swagger_auto_schema( 
    method="delete", 
    tags=["Texts/Quizs"], 
    manual_parameters=[
        openapi.Parameter('id',in_=openapi.IN_QUERY, description='id', type=openapi.TYPE_INTEGER),  
        openapi.Parameter('title',in_=openapi.IN_QUERY, description='title', type=openapi.TYPE_STRING),
    ]
)
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def deleteText(request):
    u = CustomUser.objects.get(username=request.user)
    if u.is_superuser: 
        id = request.GET.get('id')
        title = request.GET.get('title')
        if id != None:
            texte = get_object_or_404(Texts, id=id)
        elif title != None:
            texte = get_object_or_404(Texts, title=title)
        
        texte.delete()

        return Response(status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema( 
    method="delete", 
    tags=["Texts/Quizs"], 
    manual_parameters=[
        openapi.Parameter('id',in_=openapi.IN_QUERY, description='id', type=openapi.TYPE_INTEGER),  
    ]
)
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def deletePhrase(request):
    u = CustomUser.objects.get(username=request.user)
    if u.is_superuser: 
        id = request.GET.get('id')
        phrase = get_object_or_404(Phrases, id=id)
        
        phrase.delete()

        return Response(status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema( 
    method="delete", 
    tags=["Texts/Quizs"], 
    manual_parameters=[
        openapi.Parameter('id',in_=openapi.IN_QUERY, description='id', type=openapi.TYPE_INTEGER),  
    ]
)
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def deleteQuiz(request):
    u = CustomUser.objects.get(username=request.user)
    if u.is_superuser: 
        id = request.GET.get('id')
        quiz = get_object_or_404(Quizs, id=id)
        
        quiz.delete()

        return Response(status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema( 
    method="post", 
    tags=["Texts/Quizs"], 
    request_body=QuizattemptSerializer,
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def postAttempt(request):
    quiz = request.data["quiz"]
    reponse = request.data["answer"]
    success = request.data["success"]
    user = request.user
    attempt = Quizattempt(username=user, quiz=quiz, answer=reponse, success=success)
    attempt.save()
    
    return Response(
        {"message": "Success"}, status=status.HTTP_200_OK
    )


@swagger_auto_schema(method="post", tags=["Texts/Quizs"], request_body=AddTtsSerializer)
@api_view(["POST"])
def addTts(request):
    title = request.data["title"]
    audio_file = request.data["text"]
    if request.method == 'POST':
        ttsAdd = TextTts(title:=title, audio_file:=audio_file)
        ttsAdd.savef()
        
@swagger_auto_schema( method="GET", tags=["Texts/Quizs"])
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def viewResult(request):

    token_key = request.META["HTTP_AUTHORIZATION"].split(" ")[1]
    user = Token.objects.filter(key=token_key).first()
    u = CustomUser.objects.get(username=request.user)
   
    if u.is_superuser:
        QuizStats = Quizattempt.objects.all()
        QuizStats_serializer = QuizattemptSerializer(QuizStats, many=True)
        return Response(
            QuizStats_serializer.data,
            status=status.HTTP_200_OK,
        )
    else:
        QuizStats = Quizattempt.objects.get(username=u.username)
        QuizStats_serializer = QuizattemptSerializer(QuizStats)
        return Response(
            QuizStats_serializer.data,
            status=status.HTTP_200_OK,
        )