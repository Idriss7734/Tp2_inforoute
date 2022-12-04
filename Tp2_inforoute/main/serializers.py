from rest_framework import serializers

from .models import CustomUser, SettingsAccount, Texts, Quizs, TextTts, Quizattempt

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
        model = CustomUser
        fields = ("username", "password", "birthday")

class QuizsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quizs       
        fields = ("__all__")
        
class TextsSerializer(serializers.ModelSerializer):
    quizs = QuizsSerializer(many=True, read_only=True)

    class Meta:
        model = Texts
        fields = ("title", "phrase", "quizs")

class AddtextSerializer(serializers.ModelSerializer):
    class Meta:
        model = TextTts
        fields = ("title", "audio_file")

class QuizattemptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quizattempt
        fields = ("username", "quiz", "reponse")