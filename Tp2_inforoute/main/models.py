from django.db import models


# Create your models here.
class Student(models.Model):
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    joining_date = models.DateField()
    birthday = models.DateField()