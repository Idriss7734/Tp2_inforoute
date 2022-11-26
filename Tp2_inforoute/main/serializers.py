from rest_framework import serializers

from .models import User, SettingsAccount, Texts

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "password")

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "password", "birthday", "is_admin")

class SettingsAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = SettingsAccount
        fields = ("username", "old_password", "new_password", "birthday")

class TextSerializer(serializers.ModelSerializer):
    class Meta:
        model = Texts
        fields = ("__all__")
