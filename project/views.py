import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
import subprocess

@csrf_exempt
def git_alert(request):
    result = 'ping'
    if 'payload' in request.POST:
        payload = json.loads(request.POST['payload'])
        git_url = payload['repository']['clone_url']        
        command = 'git clone ' + str(git_url) 

#        subprocess.call(["git_file"], shell=True)
#        command = "git pull"

        command = command.split()
        subprocess.Popen(command, stdin=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines = True)

    result = subprocess.check_output(["python", "git_file/hello.py", "3"])  # test case

    result = int(result.decode('utf-8'))

    if result is 9:  # auto grading
        result = subprocess.check_output(["python", "git_file/hello.py", "8"])  # test case
        result = int(result.decode('utf-8'))
        if result is 64:
            result = "pass"
        else:
            result = "fail"
    else :
        result = "fail"


    return render(request, "push.html", {"result": result})

