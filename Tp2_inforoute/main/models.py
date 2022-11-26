from django.contrib.auth.models import AbstractUser
from django.db import models

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
    idText= models.FloatField()
    phrase = models.CharField(max_length=150)
    reponse1 = models.CharField(max_length=150)
    reponse2 = models.CharField(max_length=150)
    reponse3 = models.CharField(max_length=150)
    reponse4 = models.CharField(max_length=150)