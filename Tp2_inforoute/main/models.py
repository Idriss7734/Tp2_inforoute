from django.contrib.auth.models import AbstractUser
import tempfile
from gtts import gTTS
from django.core.files import File
from django.db import models
from django import forms

# Create your models here.

class CustomUser(AbstractUser):
    birthday = models.DateField()
    is_superuser = models.BooleanField(default=False)

class Texts(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=255)
    idAudio = models.IntegerField()

class Quizs(models.Model):
    id = models.IntegerField(primary_key=True)
    idText= models.IntegerField()
    question = models.CharField(max_length=150)
    reponse1 = models.CharField(max_length=150)
    reponse2 = models.CharField(max_length=150)
    reponse3 = models.CharField(max_length=150)
    reponse4 = models.CharField(max_length=150)
    idAudioQ = models.IntegerField()
    idAudioR1= models.IntegerField()
    idAudioR2= models.IntegerField()
    idAudioR3= models.IntegerField()
    idAudioR4= models.IntegerField()

class Phrases(models.Model):
    id = models.IntegerField(primary_key=True)
    idText = models.IntegerField()
    phrase = models.CharField(max_length=255)
    idAudio= models.IntegerField()

class Tts(models.Model):
    id =  models.IntegerField(primary_key=True)
    fileName = models.CharField(max_length=255)
    text = models.CharField(max_length=255)
    path = models.CharField(max_length=255)

    def saveFile(self, *args, **kargs):
        audio_file = gTTS(self.text, lang='fr')
        audio_file.save("./audio/{}.mp3".format(self.fileName))


class Quizattempt(models.Model):
    username = models.CharField(max_length=150)
    quiz = models.IntegerField()
    answer = models.IntegerField()
    success = models.IntegerField()

class ImageWords(models.Model):
    id = models.IntegerField(primary_key=True)
    word = models.TextField()
    path = models.TextField()

class ImageList(models.Model):
    id = models.IntegerField(primary_key=True)
    paths = models.CharField(max_length=255)
    idT = models.IntegerField()
    idP = models.IntegerField()
    idQ = models.IntegerField()
    numR= models.IntegerField()
        
