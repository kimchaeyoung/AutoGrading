import json
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
import subprocess
import pprint
import os
from django.views.generic import TemplateView
from django.contrib.auth.models import User

def home(request):
    return render(request, 'home.html')

def login(request):
    return render(request, 'login.html')

def student(request):
    return render(request, 'student.html')

def professor(request):
    return render(request, 'professor.html')

class UsersView(TemplateView):
    template_name='studentlist.html'

    def get_context_data(self,**kwargs):
        context = super(UsersView,self).get_context_data(**kwargs)
        context['object_list'] = User.objects.all()
        return context

def classroom(request):
    return render(request, 'class.html')   

@csrf_exempt
def git_alert(request):
    result = 'pingping'
    if 'payload' in request.POST:
        payload = json.loads(request.POST['payload'])

        if payload['created'] is True:
            result = "created"
            clone_url = payload['repository']['clone_url']
            
            command = 'git clone ' + str(clone_url) 
            command = command.split()
            subprocess.Popen(command, stdin=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines = True)

        else:
            result = "push"
            cwd = os.getcwd()
            os.chdir(cwd + '/git_files')
            command = 'git pull'
            command = command.split()
            subprocess.call(command)
            os.chdir(cwd)


    return render(request, "push.html", {})

def test_code(request):
   #result = subprocess.check_output(["python", "git_files/hello.py"])
   # result = int(result.decode('utf-8'))

   command = "python git_files/hello.py"
   command = command.split()
   p = subprocess.Popen(command, stdin=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines = True)
   result = p.communicate('3')
   
   print(result)


   ''' 
    if result is 9:
        result = subprocess.check_output(["python", "git_files/hello.py", "8"])
        result = int(result.decode('utf-8'))
        if result is 64:
            result = "pass"
        else:
            result = "fail"
   '''
   if result is 9 :
        result = "pass"
   else:
        result = "fail"

   return JsonResponse(result, safe=False)


     



