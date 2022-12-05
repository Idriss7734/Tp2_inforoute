from rest_framework import serializers

from .models import CustomUser, SettingsAccount, Texts, Quizs, TextTts, Quizattempt, Phrases

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

class PhrasesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Phrases
        fields = ("idText", "phrase")

class QuizsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quizs       
        fields = ("question", "reponse1", "reponse2", "reponse3", "reponse4")
       
class addQuiz(serializers.ModelSerializer):
    class Meta:
        model = Quizs       
        fields = ("idText", "question", "reponse1", "reponse2", "reponse3", "reponse4")

class TextsSerializer(serializers.ModelSerializer):
    quizs = QuizsSerializer(many=True, read_only=True)
    phrases = PhrasesSerializer(many=True, read_only=True)

    class Meta:
        model = Texts
        fields = ("title", "phrases", "quizs")

class addTextSerializer(serializers.ModelSerializer):
    class Meta:
        model = Texts
        fields = ("title",)

class modifyTextSerializer(serializers.ModelSerializer):
    class Meta:
        model = Texts
        fields = ("id", "title")

class modifyPhraseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Phrases
        fields = ("id", "phrase")

class putPhraseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Phrases
        fields = ("phrase",)

class modifyQuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quizs
        fields = ("id", "question", "reponse1", "reponse2", "reponse3", "reponse4")

class AddTtsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TextTts
        fields = ("title", "audio_file")

class QuizattemptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quizattempt
        fields = ("username", "quiz", "answer", "success")