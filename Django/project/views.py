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
from django.core import serializers

def home(request):
    return render(request, 'home.html')

def signup_form(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data
            if user['isManager'] == False:
                if not Student.objects.filter(student_id=user['id']).exists():
                    s = Student(student_id=user['id'], student_name=user['name'])
                    s.save()
                    return render(request, 'registration/login.html')
                else:
                    return HttpResponse("invalid id, already exists")
            else:
                if not Professor.objects.filter(professor_id=user['id']).exists():
                    p = Professor(professor_id=user['id'], professor_name=user['name'])
                    p.save()
                    return HttpResponse("successfully applied! "+str(user['name'])+", please wait until your account is approved.")
                else:
                    return HttpResponse("invalid id, already exists")
    else:
            form = SignUpForm()

    return render(request, 'form.html', {'form':form})

def login(request):
        
    return render(request, 'login.html')

def success_login(request):
    current_user=request.user
    if Student.objects.filter(student_id=current_user).exists():
        s = Student.objects.get(student_id=current_user)
        if not Homework_student.objects.filter(student=s).exists():
            my_hws = "No accepted homeworks yet"
        else :
            my_hws = Homework_student.objects.filter(student=s)
        return render(request, 'student.html', {'hws':my_hws})
    elif Professor.objects.filter(professor_id=current_user).exists():
        p = Professor.objects.get(professor_id=current_user)
        if p.status == True:
            hws = None
            pmslist = None
            if Professor.objects.filter(status=False).exists():
                pmslist = Professor.objects.filter(status=False)
            if Homework.objects.filter(madeby=current_user).exists():
                hws = Homework.objects.filter(madeby=current_user)
            return render(request, 'professor.html', {'hws':hws, 'pmslist':pmslist})
        else:
            return HttpResponse("Sorry, you are not yet approved as manager.")
    elif str(current_user)=="admin":
        return HttpResponse("You are system manager. Go to the admin page.")
    else:
        return HttpResponse("Please sign up first")

def permission(request, userid):
    current_user=request.user
    if Professor.objects.filter(professor_id=current_user).exists():
        p = Professor.objects.get(professor_id=userid)
        p.status = True;
        p.save()
        return HttpResponse("Done")
    else :
        return HttpResponse("You don't have permission to access this page")

def managehw(request, hwname):
    h = Homework.objects.get(hwname=hwname)
    hws = Homework_student.objects.filter(homework=h)
    return render(request, 'managehws.html', {'hws':hws, 'h':h})

def hwinfo(request, hwname):
    if request.method == 'POST':
        form = HWInfo(request.POST)
        if form.is_valid():
            hwinfo = form.cleaned_data
            h = Homework.objects.get(hwname=hwname)
            h.link = hwinfo['link']
            h.duedate = hwinfo['datetime']
            h.save()
            return HttpResponse("Updated!")
        else:
            return HttpResponse("Wrong information")
    else:
        form = HWInfo()
    
    return render(request, 'hwinfo.html', {'form':form})    


def student(request):
    current_user=request.user
    if Student.objects.filter(student_id=current_user).exists():
       s = Student.objects.get(student_id=current_user)
       hw = None
       if not Homework_student.objects.filter(student=s).exists():
           my_hws = "No accepted homeworks yet"
       else :
           my_hws = Homework_student.objects.filter(student=s)
           hw = serializers.serialize('json',my_hws)
       return HttpResponse(hw, content_type="text/json-comment-filtered")
    return HttpResponse()

#def professor(request):
#    if request.user != None:
#        professor = request.user.username
#        if not Professor.objects.filter(professor_id=professor).exists():
#            p=Professor(professor_id=professor, professor_name=professor)
#            p.save()
#            print(professor)
#    return render(request, 'professor.html')

#class UsersView(TemplateView):
#    template_name='studentlist.html'

#    def get_context_data(self,**kwargs):
#        context = super(UsersView,self).get_context_data(**kwargs)
#        context['object_list'] = User.objects.all()
#        return context

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
#            result=run_code(payload['repository']['name'])
        else: 
            result = "push"
            print("x")
            cwd = os.getcwd()
            os.chdir(cwd + '/' + payload['repository']['name'])
            command = 'git pull'
            command = command.split()
            subprocess.call(command)
            os.chdir(cwd)
#            result=run_code(payload['repository']['name'])
#    print(result)
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
            h = Homework.objects.get(hwname=words[0].upper())
            s = Student.objects.get(student_id=words[1])
            if action=="created":
                if not Homework_student.objects.filter(homework=h).filter(student=s).exists():
                    hs = Homework_student(homework=h, student=s)
                    hs.save()
#            elif action=="deleted":
#                if Homework_student.objects.filter(homework=words[0].upper()).filter(student=words[1]).exists():
#                    hs = Homework_student(homework=words[0].upper(), student=words[1],homework_name=hwname)
#                    hs.delete()

 
        else: #교수님이 문제를 내서 rp가 create 되었을때 / 교수님께 HW name에 절대 - 를 포함해서는 안된다고 안내해야함 - 별로다...

            if action=="created":
                if not Homework.objects.filter(hwname=hwname.upper()).exists():
                    h = Homework(hwname=hwname.upper(), madeby=payload['sender']['login'])
                    h.save()
 #           elif action=="deleted":
 #               if Homeworks.objects.filter(hw_name=hwname).exists():
 #                   h = Homeworks.objects.get(hw_name=hwname)
 #                   h.delete()

    return HttpResponse("Done")        


def run_code(request,repository_name):
    MyOut = subprocess.Popen('./runcode.sh ' + repository_name, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    stdout, stderr = MyOut.communicate()
    if stdout is not None:
        stdout = stdout.decode('utf-8')
    if stderr is not None:
        stderr = stderr.decode('utf-8')

    with open('input_output/output.txt', 'r') as f:
        data = f.read().replace('\n','')
    if stderr is not None:
        print("stderr")
        return JsonResponse(str(stderr), safe=False)
    elif stdout == data:
        print("success")
        return JsonResponse(str("success"), safe=False)
    elif stdout is not data:
        print("fail")
        return JsonResponse(str("fail"), safe=False)
