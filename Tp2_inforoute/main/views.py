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

from .models import CustomUser, Texts, Tts, Quizs, Quizattempt, Phrases, ImageWords, ImageList
from .serializers import LoginSerializer, RegisterSerializer, SettingsAccountSerializer, TextsSerializer, QuizsSerializer, AddTtsSerializer, QuizattemptSerializer, PhrasesSerializer, addTextSerializer, addQuizSerializer, modifyTextSerializer, modifyPhraseSerializer, modifyQuizSerializer, ImageWordsSerializer


@swagger_auto_schema(
    method="post", tags=["Register"], request_body=RegisterSerializer
)
@api_view(["POST", "GET"])
def register(request):
    if request.method == "GET":
        return render(request, "Tp/register.html", {"status": False})
    elif request.method == "POST":
        username = request.data["username"]
        password = request.data["password"]
        birthday = request.data["birthday"]
        user = CustomUser(username=username, password=make_password(password), birthday=birthday)
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
@permission_classes([IsAuthenticated])
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
    text = Texts.objects.filter(title = textTitle).first()
    text_seri = TextsSerializer(text, many=True)
    phrases = Phrases.objects.filter(idText=text.id)#text[:1] = premier champ d'un element de type text, ce qui donne l'id
    phrase_seri = PhrasesSerializer(phrases, many=True)
    quizs = Quizs.objects.filter(idText = text.id) #text[:1] = premier champ d'un element de type text, ce qui donne l'id
    quiz_seri = QuizsSerializer(quizs, many=True)

    titleImages = ImageList.objects.filter(idT = text.id).first().paths
    
    pathAudio = Tts.objects.filter(id=text.idAudio).first().path
    dictT = {"title": [text.title], "paths": [titleImages], "pathAudio": [pathAudio]}

    dictP = {"phrase": [], "paths": [], "pathsAudio": []}
    for p in phrases:
        dictP["phrase"].append(p.phrase)
        dictP["paths"].append(ImageList.objects.filter(idP = p.id).first().paths)
        dictP["pathsAudio"].append(Tts.objects.filter(id=p.idAudio).first().path)

    
    dictQ = {"question": [], "qPaths": [], "r1": [], "r1Paths": [], "r1PathsAudio": [], "r2": [], "r2Paths": [], "r2PathsAudio": [], "r3": [], "r3Paths": [], "r3PathsAudio": [], "r4": [], "r4Paths": [], "r4PathsAudio": [],}
    for q in quizs:
        dictQ["question"].append(q.question)
        dictQ["qPaths"].append(ImageList.objects.filter(idQ = q.id, numR=None).first().paths)
        dictQ["r1"].append(q.reponse1)
        dictQ["r1Paths"].append(ImageList.objects.filter(idQ = q.id, numR=1).first().paths)
        dictQ["r1PathsAudio"].append(Tts.objects.filter(id=q.idAudioR1).first().path)
        dictQ["r2"].append(q.reponse2)
        dictQ["r2Paths"].append(ImageList.objects.filter(idQ = q.id, numR=2).first().paths)
        dictQ["r2PathsAudio"].append(Tts.objects.filter(id=q.idAudioR2).first().path)
        dictQ["r3"].append(q.reponse3)
        dictQ["r3Paths"].append(ImageList.objects.filter(idQ = q.id, numR=3).first().paths)
        dictQ["r3PathsAudio"].append(Tts.objects.filter(id=q.idAudioR3).first().path)
        dictQ["r4"].append(q.reponse4)
        dictQ["r4Paths"].append(ImageList.objects.filter(idQ = q.id, numR=4).first().paths)
        dictQ["r4PathsAudio"].append(Tts.objects.filter(id=q.idAudioR4).first().path)

    return Response(
        {"-Title": dictT, "-Phrases": dictP, "-Quizs": dictQ}, status=status.HTTP_200_OK
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
        
        id = createAudio(textTitle)

        text = Texts(title=textTitle, idAudio = id)
        text.save()

        id = Texts.objects.filter(title=textTitle).first().id
        linkImages(textTitle, "t", id, None)

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

        id = createAudio(phraseInput)

        phrase = Phrases(idText=idText, phrase=phraseInput, idAudio=id)
        phrase.save()

        id = Phrases.objects.filter(idText=idText, phrase=phraseInput).first().id
        linkImages(phraseInput, "p", id, None)

        return Response(
            {"message": "Success"}, status=status.HTTP_200_OK
        )
    
    return Response(
        {"message": "Error: Not admin"}, status=status.HTTP_200_OK
    )

@swagger_auto_schema( 
    method="post", 
    tags=["Texts/Quizs"], 
    request_body=addQuizSerializer,
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

        idAudioQ = createAudio(question)
        idAudioR1 = createAudio(reponse1)
        idAudioR2 = createAudio(reponse2)
        idAudioR3 = createAudio(reponse3)
        idAudioR4 = createAudio(reponse4)


        quiz = Quizs(idText=idText, question=question, reponse1=reponse1, reponse2=reponse2, reponse3=reponse3, reponse4=reponse4, idAudioQ=idAudioQ, idAudioR1=idAudioR1, idAudioR2=idAudioR2, idAudioR3=idAudioR3, idAudioR4=idAudioR4)
        quiz.save()

        id = Quizs.objects.filter(idText=idText, question=question, reponse1=reponse1, reponse2=reponse2, reponse3=reponse3, reponse4=reponse4).first().id
        
        #question
        linkImages(question, "q", id, None)
        #answers
        linkImages(reponse1, "r", id, 1)
        linkImages(reponse2, "r", id, 2)
        linkImages(reponse3, "r", id, 3)
        linkImages(reponse4, "r", id, 4)
        


        return Response(
            {"message": "Success"}, status=status.HTTP_200_OK
        )
    
    return Response(
        {"message": "Error: Not admin"}, status=status.HTTP_200_OK
    )

@swagger_auto_schema( 
    method="put", 
    tags=["Texts/Quizs"], 
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
            id = request.GET.get('id')

            title = request.GET.get('title')
            texts = Texts.objects.all()

            for t in texts:
                if t.id == int(id):
                    text = t  

            data = {'title': text.title, 'idAudio': text.idAudio}

            if title != None:
                data['title'] = title
                idAudio = createAudio(title)
                data['idAudio'] = idAudio
            

            text_seri = addTextSerializer(text, data=data)
            if not text_seri.is_valid():
                return Response("data is invalid", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            linkToRemove = ImageList.objects.filter(idT = id).first()
            removeLink(linkToRemove.id)
            linkImages(title, "t", id, None)

            text_seri.save()
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response("The user not an admin", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@swagger_auto_schema( method="put", tags=["Texts/Quizs"],
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
            id = request.GET.get('id')

            newPhrase = request.GET.get('phrase')
            phrases = Phrases.objects.all()

            for p in phrases:
                if p.id == int(id):
                    phrase = p  

            data = {'phrase': phrase.phrase, 'idAudio': phrase.idAudio}

            if newPhrase != None:
                data['phrase'] = newPhrase
                idAudio = createAudio(newPhrase)
                data['idAudio'] = idAudio

            

            phrase_seri = modifyPhraseSerializer(phrase, data=data)
            
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            if not phrase_seri.is_valid():
                return Response({"message": "invalid data in serializer"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            linkToRemove = ImageList.objects.filter(idP = id).first()
            removeLink(linkToRemove.id)
            linkImages(newPhrase, "p", id, None)

            phrase_seri.save()
            return Response(status=status.HTTP_200_OK)
        except:
            return Response("invalid data",status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response("The user not an admin",status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@swagger_auto_schema( method="put", tags=["Texts/Quizs"],
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
        # try:
        if True:
            qu = False
            r1 = False
            r2 = False
            r3 = False
            r4 = False
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

            data = {'question': quiz.question, 'reponse1': quiz.reponse1, 'reponse2': quiz.reponse2, 'reponse3': quiz.reponse3, 'reponse4': quiz.reponse4, 'idAudioQ': quiz.idAudioQ, 'idAudioR1': quiz.idAudioR1, 'idAudioR2': quiz.idAudioR2, 'idAudioR3': quiz.idAudioR3, 'idAudioR4': quiz.idAudioR4}

            if question != None:
                data['question'] = question
                qu = True
                data['idAudioQ'] = createAudio(question)

            if reponse1 != None:
                data['reponse1'] = reponse1
                r1 = True
                data['idAudioR1'] = createAudio(reponse1)
            
            if reponse2 != None:
                data['reponse2'] = reponse2
                r2 = True
                data['idAudioR2'] = createAudio(reponse2)

            if reponse3 != None:
                data['reponse3'] = reponse3
                r3 = True
                data['idAudioR3'] = createAudio(reponse3)

            if reponse4 != None:
                data['reponse4'] = reponse4
                r4 = True
                data['idAudioR4'] = createAudio(reponse4)
                
            quiz_seri = modifyQuizSerializer(quiz, data=data)
            if not quiz_seri.is_valid():
                return Response({"data is invalid"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


            #images
            if qu:
                linkToRemove = ImageList.objects.filter(idQ = id, numR=None).first()
                removeLink(linkToRemove.id)
                linkImages(question, "q", id, None)
            if r1:
                linkToRemove = ImageList.objects.filter(idQ = id, numR=1).first()
                removeLink(linkToRemove.id)
                linkImages(reponse1, "r", id, 1)
            if r2:
                linkToRemove = ImageList.objects.filter(idQ = id, numR=2).first()
                removeLink(linkToRemove.id)
                linkImages(reponse2, "r", id, 2)
            if r3:
                linkToRemove = ImageList.objects.filter(idQ = id, numR=3).first()
                removeLink(linkToRemove.id)
                linkImages(reponse3, "r", id, 3)
            if r4:
                linkToRemove = ImageList.objects.filter(idQ = id, numR=4).first()
                removeLink(linkToRemove.id)
                linkImages(reponse4, "r", id, 4)

            quiz_seri.save()
            return Response(status=status.HTTP_200_OK)
        # except:
        #     return Response("The user id is invalid.",status=status.HTTP_500_INTERNAL_SERVER_ERROR)
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

@swagger_auto_schema( method="get", tags=["Images"])
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getImageWords(request):
    imageWords = ImageWords.objects.all()
    imageWords_seri = ImageWordsSerializer(imageWords, many=True)
    return Response(
        {"message": "{}".format(imageWords_seri.data)}, status=status.HTTP_200_OK
    )

@swagger_auto_schema( 
    method="post", 
    tags=["Images"], 
    request_body=ImageWordsSerializer,
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def addImageWord(request):
    u = CustomUser.objects.get(username=request.user)
    
    if u.is_superuser:
        word = request.data["word"]
        path = "./ressource/" + request.data["path"]

        imageWord = ImageWords(word=word, path=path)
        imageWord.save()
        return Response(
            {"message": "Success"}, status=status.HTTP_200_OK
        )
    
    return Response(
        {"message": "Error: Not admin"}, status=status.HTTP_400_BAD_REQUEST
    )

@swagger_auto_schema( 
    method="delete", 
    tags=["Images"], 
    manual_parameters=[
        openapi.Parameter('word',in_=openapi.IN_QUERY, description='word', type=openapi.TYPE_STRING),  
    ]
)
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def deleteImageWord(request):
    u = CustomUser.objects.get(username=request.user)
    if u.is_superuser: 
        wordInput = request.GET.get('word')
        word = get_object_or_404(ImageWords, word=wordInput)
        
        word.delete()

        return Response(status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(method="post", tags=["TTS"], request_body=AddTtsSerializer)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def addTts(request):
    u = CustomUser.objects.get(username=request.user)
    if u.is_superuser:
        fileName = request.data["fileName"]
        text = request.data["text"]
        if createAudio(fileName, text):
            return Response(status=status.HTTP_200_OK)
        else:
            Response({"message": "file already exists"},status=status.HTTP_400_BAD_REQUEST)        
    return Response(status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(method="delete", tags=["TTS"], 
    manual_parameters=[
        openapi.Parameter('id',in_=openapi.IN_QUERY, description='id', type=openapi.TYPE_STRING),  
    ]
)
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def deleteTts(request):
    u = CustomUser.objects.get(username=request.user)
    if u.is_superuser: 
        id = request.GET.get("id")
        file = get_object_or_404(Tts, id=id)
        
        file.delete()
        
        return Response(status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)
    
        
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
        QuizStats = Quizattempt.objects.filter(username=u.username)

        dictQ = {"Result": [],}
        for i in QuizStats:
            QuizStats_serializer = QuizattemptSerializer(i)
            dictQ["Result"].append(QuizStats_serializer.data) 
        
        return Response(
            dictQ,
            status=status.HTTP_200_OK,
        )


def createAudio(fileName):
    fileName = fileName.replace(".", "")
    fileName = fileName.replace("?", "")
    fileName = fileName.lower()
    if not Tts.objects.filter(fileName = fileName).exists():
        file = Tts(fileName = fileName, text = fileName, path = "./audio/{}.mp3".format(fileName))
        file.save()
        file.saveFile()
        id = Tts.objects.filter(fileName = fileName).first().id
        return id
    else:
        return Tts.objects.filter(fileName = fileName).first().id
    

def linkImages(string, type, id, numR):
    string = string.replace(".", "")
    string = string.replace("?", "")
    words = ImageWords.objects.all()
    string = string.lower()
    string = string.split()
    dict = {"words": [], "paths": []}

    for s in string:
        for w in words:
            if s == w.word:
                dict["words"].append(w.word)
                dict["paths"].append(w.path)

    if dict == {"words": [], "paths": []}:
        dict = "no image"
    
    match type:
        case "t": #title
            images = ImageList(paths = dict, idT=id)
        case "p":#phrase
            images = ImageList(paths = dict, idP=id)
        case "q":#quiz
            images = ImageList(paths = dict, idQ=id)
        case "r":#reponse
            images = ImageList(paths = dict, idQ=id, numR=numR)

    images.save()

def removeLink(id):
    link = get_object_or_404(ImageList, id=id)
    link.delete()