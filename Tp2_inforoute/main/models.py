from django.contrib.auth.models import AbstractUser
import tempfile
from gtts import gTTS
from django.core.files import File
from django.db import models
from django import forms

# Create your models here.

class CustomUser(AbstractUser):
    birthday = models.DateField()

class SettingsAccount(models.Model):
    username = models.CharField(max_length=30)
    old_password = models.CharField(max_length=30)
    new_password = models.CharField(max_length=30)
    birthday = models.DateField()

class Texts(models.Model):
    title = models.CharField(max_length=30)
    phrase = models.CharField(max_length=150)

class Quizs(models.Model):
    idText= models.IntegerField()
    phrase = models.CharField(max_length=150)
    reponse1 = models.CharField(max_length=150)
    reponse2 = models.CharField(max_length=150)
    reponse3 = models.CharField(max_length=150)
    reponse4 = models.CharField(max_length=150)

class TextTts(models.Model):
    title = models.CharField(max_length=255)
    audio_file = models.FileField(upload_to='audio/')

    def savef(self, *args, **kwargs):
        audio_file = gTTS(title=self.title, lang='fr')
        with tempfile.TemporaryFile() as f:
            audio_file.write_to_fp(f)
            file_name = '{}.mp3'.format(self.title)
            self.audio_file.save(file_name, File(file=f))
            self.audio_file = File(file=f)
           
class Quizattempt(models.Model):
    username = models.CharField(max_length=150)
    quiz = models.IntegerField()
    reponse = models.IntegerField()
        
