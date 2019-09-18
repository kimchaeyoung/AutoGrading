from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import AbstractUser

class Homeworks(models.Model):
    hw_name = models.CharField(max_length=200)

class Homework_student(models.Model):
    homework = models.CharField(max_length=200)
    student = models.CharField(max_length=200)
    homework_name = models.CharField(max_length=200)
    score = models.CharField(max_length=200, default="Waiting")

class Professor(models.Model):
    professor_id = models.CharField(max_length=50)
    professor_name = models.CharField(max_length=50)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.professor_name

class Student(models.Model):
    student_id = models.CharField(max_length=50)
    student_name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.student_name
