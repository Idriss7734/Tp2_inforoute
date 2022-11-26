from rest_framework import serializers

from .models import CustomUser, SettingsAccount, Texts, Quizs, TextTts

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("username", "password")

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("username", "password", "birthday", "is_superuser")

class SettingsAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = SettingsAccount
        fields = ("username", "old_password", "new_password", "birthday")

class TextsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Texts
        fields = ("__all__")

class QuizsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quizs
        fields = ("__all__")

class AddtextSerializer(serializers.ModelSerializer):
    class Meta:
        model = TextTts
        fields = ("title", "audio_file")