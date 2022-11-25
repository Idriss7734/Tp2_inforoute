from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Student

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "password")

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ("username", "password","birthday")