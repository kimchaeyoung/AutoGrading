from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import AbstractUser


class Classrooms(models.Model):
    organization = models.CharField(max_length=200)

class Homeworks(models.Model):
    classroom = models.ForeignKey(Classrooms, on_delete=models.CASCADE)
    hw_name = models.CharField(max_length=200)


class Classroom_student(models.Model):
    classroom = models.CharField(max_length=200)
    student = models.CharField(max_length=200)

class Homework_student(models.Model):
    homework = models.CharField(max_length=200)
    student = models.CharField(max_length=200)
    homework_name = models.CharField(max_length=200)

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
