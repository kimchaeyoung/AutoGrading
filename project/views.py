import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import pprint
import subprocess

@csrf_exempt
def git_alert(request):
    if 'payload' in request.POST:
        payload = json.loads(request.POST['payload'])
        git_url = payload['repository']['clone_url']
        
        command = 'git clone ' + str(git_url) 
        command = command.split()
        
        subprocess.Popen(command, stdin=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines = True)
        
    return HttpResponse('pong')
