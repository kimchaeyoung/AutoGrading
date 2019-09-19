from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import AbstractUser

class Homework(models.Model):
    hwname = models.CharField(max_length=200, primary_key=True) #always upper letter
    madeby = models.CharField(max_length=200)
    link = models.CharField(max_length=200, blank=True, null=True)
    duedate = models.DateTimeField(blank=True, null=True)

class Student(models.Model):
    student_id = models.CharField(max_length=50)
    student_number = models.IntegerField(default=0)
    student_name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.student_name

class Homework_student(models.Model):
    homework = models.ForeignKey(Homework, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    score = models.CharField(max_length=200, default="Wating")

class Professor(models.Model):
    professor_id = models.CharField(max_length=50)
    professor_name = models.CharField(max_length=50)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.professor_name


