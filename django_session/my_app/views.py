import os
import string
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponseServerError
from django.views.decorators.http import require_GET

SECRETS_PATH = os.path.join(settings.BASE_DIR, 'secrets')
ALLOWED_CHARACTERS = string.ascii_letters + string.digits + '/'


os.makedirs(SECRETS_PATH, exist_ok=True)


sample_path = os.path.join(SECRETS_PATH, 'sample')
with open(sample_path, 'w') as f:
    f.write('Hello, world :)')

flag_dir = os.path.join(SECRETS_PATH, os.urandom(32).hex())
os.makedirs(flag_dir, exist_ok=True)
flag_path = os.path.join(flag_dir, 'flag')
try:
   
    with open('/flag', 'r') as f0, open(flag_path, 'w') as f1:
        f1.write(f0.read())
except Exception:
   
    with open(flag_path, 'w') as f1:
        f1.write('FLAG_NOT_FOUND')

@require_GET
def index(request):
 
    request.session['secret'] = flag_path

 
    path = request.GET.get('path', '')
    if not isinstance(path, str) or path == '':
        return render(request, 'index.html', {'msg': 'input the path!'})


    if any(ch not in ALLOWED_CHARACTERS for ch in path):
        return render(request, 'index.html', {'msg': 'invalid path!'})


    full_path = os.path.join(SECRETS_PATH, path)
    if not os.path.isfile(full_path):
        return render(request, 'index.html', {'msg': 'invalid path!'})

    try:
        with open(full_path, 'r') as f:
            content = f.read()
        return render(request, 'index.html', {'msg': content})
    except Exception:
        return HttpResponseServerError("Internal Server Error")