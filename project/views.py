import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
import subprocess
import pprint
import os

@csrf_exempt
def git_alert(request):
    global final_result
    result = 'pingping'
    if 'payload' in request.POST:
        payload = json.loads(request.POST['payload'])
        pprint.pprint(payload)
        print(payload['created'])
        if payload['created'] is True:
            result = "created"
            print("o")
            clone_url = payload['repository']['clone_url']
            command = 'git clone ' + str(clone_url) 
            command = command.split()
            subprocess.Popen(command, stdin=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines = True)

        else:
            result = "push"
            print("x")
            cwd = os.getcwd()
            os.chdir(cwd + '/' + payload['repository']['name'])
            command = 'git pull'
            command = command.split()
            subprocess.call(command)
            os.chdir(cwd)

            run_code(payload['repository']['name'])

    return render(request, "push.html", {"result": result})

def run_code(repository_name):
    print(repository_name)
    MyOut = subprocess.Popen('./runcode.sh '+ repository_name,
            stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT,
            shell = True)
    stdout,stderr = MyOut.communicate()
    if stdout is not None:
        stdout = stdout.decode('UTF-8')
    if stderr is not None:
        stderr = stderr.decode('UTF-8')
    print(stdout)
    print(stderr)

    with open('input_output/output.txt', 'r') as f:
        data = f.read().replace('\n','') 
        print('**'+data)

    if stderr is not None:
        print('error')
        return stderr

    elif stdout == data:
        print('success')
        return 'success'
    elif stdout is not data:
        print('fail')
        return 'fail'
