from rest_framework import serializers

from .models import CustomUser, Texts, Quizs, Tts, Quizattempt, Phrases, ImageWords

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
       
class addQuizSerializer(serializers.ModelSerializer):
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
        fields = ("title", "idAudio")

class modifyTextSerializer(serializers.ModelSerializer):
    class Meta:
        model = Texts
        fields = ("id", "title")

class modifyPhraseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Phrases
        fields = ("id", "phrase", "idAudio")

class modifyQuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quizs
        fields = ("question", "reponse1", "reponse2", "reponse3", "reponse4", "idAudioQ", "idAudioR1", "idAudioR2", "idAudioR3", "idAudioR4")

class AddTtsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tts
        fields = ("fileName", "text")

class QuizattemptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quizattempt
        fields = ("username", "quiz", "answer", "success")

class ImageWordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageWords
        fields = ("word", "path")