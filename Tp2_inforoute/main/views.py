from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token

from drf_yasg.utils import swagger_auto_schema

from .serializers import LoginSerializer

def register(request):
    if request.method == "GET":
        return render(request, "Tp/register.html", {"status": False})
    elif request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = User(username=username, password=make_password(password))
        user.save()

        return render(request, "Tp/register.html", {"status": True})




@swagger_auto_schema(
    method="post", tags=["Authentication"], request_body=LoginSerializer
)
@api_view(["POST"])
def login(request):
    username = request.data["username"]
    password = request.data["password"]

    user = User.objects.filter(username=username)

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

