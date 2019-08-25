import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
import subprocess
import pprint
import os

@csrf_exempt
def git_alert(request):
    result = 'pingping'
    if 'payload' in request.POST:
        payload = json.loads(request.POST['payload'])
        pprint.pprint(payload)
        print(payload['created'])
        if payload['created'] is True:
            result = "created"
            print("o")
            #student_name = payload['commits']['author']['name']
            clone_url = payload['repository']['clone_url']
            #subprocess.call(['mkdir', student_name])
            #subprocess.call(['cd', student_name])
            
            command = 'git clone ' + str(clone_url) 
            command = command.split()
            subprocess.Popen(command, stdin=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines = True)

        else:
            result = "push"
            print("x")
            cwd = os.getcwd()
            os.chdir(cwd + '/test6')
            command = 'git pull'
            command = command.split()
            subprocess.call(command)
            os.chdir(cwd)


    return render(request, "push.html", {"result": result})

