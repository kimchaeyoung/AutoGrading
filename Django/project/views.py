import json
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
import subprocess
import pprint
import os
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from .models import *
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .forms import *

def signup_form(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data
            if user['isManager'] == False:
                s = Student(student_id=user['id'], student_name=user['name'])
                s.save()
                return render(request, 'registration/login.html')
            else:
                p = Professor(professor_id=user['id'], professor_name=user['name'])
                p.save()
                return HttpResponse("successfully applied! "+str(user['name'])+", please wait until your account is approved.")
    else:
            form = SignUpForm()

    return render(request, 'form.html', {'form':form})

def home(request):
    return render(request, 'home.html')

def login(request):
        
    return render(request, 'login.html')

def success_login(request):
    current_user=request.user
    if Student.objects.filter(student_id=current_user).exists():
        return render(request, 'student.html')
    elif Professor.objects.filter(professor_id=current_user).exists():
        p = Professor.objects.get(professor_id=current_user)
        if p.status == True:
            return render(request, 'professor.html')
        else:
            return HttpResponse("Sorry, you are not yet approved as manager.")
    else:
        return render(request, 'home.html')

def student(request):
    return render(request, 'student.html')

def professor(request):
    if request.user != None:
        professor = request.user.username
        if not Professor.objects.filter(professor_id=professor).exists():
            p=Professor(professor_id=professor, professor_name=professor)
            p.save()
            print(professor)
    return render(request, 'professor.html')

def check_task(request):
    return render(request, 'check_task.html')

def mypage(request):
    current_user=request.user
    data = Student.objects.get(name=current_user.username)
    return render(request, 'mypage.html', {'student': data})

class UsersView(TemplateView):
    template_name='studentlist.html'

    def get_context_data(self,**kwargs):
        context = super(UsersView,self).get_context_data(**kwargs)
        context['object_list'] = User.objects.all()
        return context

def classroom(request):
    return render(request, 'class.html')   

@csrf_exempt
def webhook(request):
    result="before grading"
    if 'payload' in request.POST:
        payload = json.loads(request.POST['payload'])
        if payload['created'] is True:
            clone_url = payload['repository']['clone_url']
            command = 'git clone ' + str(clone_url)
            command = command.split()
            subprocess.Popen(command, stdin=subprocess.PIPE, stderr = subprocess.PIPE, universal_newlines = True)
            result=run_code(payload['repository']['name'])
        else: 
            result = "push"
            print("x")
            cwd = os.getcwd()
            os.chdir(cwd + '/' + payload['repository']['name'])
            command = 'git pull'
            command = command.split()
            subprocess.call(command)
            os.chdir(cwd)
            result=run_code(payload['repository']['name'])
    print(result)
    return HttpResponse(result)


@csrf_exempt
def createhw(request):
    if 'payload' in request.POST:
        payload = json.loads(request.POST['payload'])
        action = payload['action']
        hwname = payload['repository']['name']
        organization = payload['repository']['owner']['login']
       
        if '-' in hwname: #학생이 hw을 accept해서 rp가 create되었을 때
            words = hwname.split("-")

            if action=="created":
                if not Classroom_student.objects.filter(classroom=organization).filter(student=words[1]).exists():
                    cs = Classroom_student(classroom=organization, student=words[1])
                    cs.save()
                    if not Homework_student.objects.filter(homework=words[0].upper()).filter(student=words[1]).exists():
                        hs = Homework_student(homework=words[0].upper(), student=words[1])
                        hs.save()

            elif action=="deleted":
                if Homework_student.objects.filter(homework=words[0].upper()).filter(student=words[1]).exists():
                    hs = Homework_student(homework=words[0].upper(), student=words[1])
                    hs.delete()

 
        else: #교수님이 문제를 내서 rp가 create 되었을때 / 교수님께 HW name에 절대 - 를 포함해서는 안된다고 안내해야함 - 별로다...

 
            if action=="created":
                if Classrooms.objects.filter(organization=organization).exists():
                    c = Classrooms.objects.get(organization=organization)
                else:
                    c = Classrooms(organization=organization)
                    c.save()
                h = Homeworks(classroom=c, hw_name=hwname)
                h.save()

            elif action=="deleted":
                if Classrooms.objects.filter(organization=organization).exists():
                    if Homeworks.objects.filter(hw_name=hwname).exists():
                        h = Homeworks.objects.get(hw_name=hwname)
                        h.delete()

    hws = Homeworks.objects.all()
    return render(request, "hwlist.html", {'hws':hws})
            

def myhw(request):
        my_hws = Homework_student.objects.get(student="joyful96")
        return render(request, "myhw.html", {'hws':my_hws})


def run_code(repository_name):
    MyOut = subprocess.Popen('./runcode.sh ' + repository_name, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    stdout, stderr = MyOut.communicate()
    if stdout is not None:
        stdout = stdout.decode('utf-8')
    if stderr is not None:
        stderr = stderr.decode('utf-8')

    with open('input_output/output.txt', 'r') as f:
        data = f.read().replace('\n','')
    if stderr is not None:
        return stderr
    elif stdout == data:
        return 'success'
    elif stdout is not data:
        return 'fail'
