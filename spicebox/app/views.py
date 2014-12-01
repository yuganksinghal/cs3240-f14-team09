from django.http import HttpResponse
from django.template import RequestContext, loader
from models import Bulletin
from forms import BulletinForm
from django.contrib.auth import authenticate, login

def login(request):
    template = loader.get_template('login.html')
    context = RequestContext(request)
    return HttpResponse(template.render(context))
      
def home(request):
    bulletins = Bulletin.objects.order_by('-pub_date')
    files = []
    for f in bulletins:
        files.extend(f.file_set.all())
    template = loader.get_template('home.html')
    context = RequestContext(request, {
        'bulletins':bulletins,
        'files':files
    })
    return HttpResponse(template.render(context))
def post_Bulletin(request):
    if(request.method== 'POST'):
        form = BulletinForm(request.POST,request.FILES)
        if(form.is_valid()):
            b = Bulletin()
            b.author = form.cleaned_data['author']
            b.description = form.cleaned_data['description']
            b.pub_date = form.cleaned_data['pubdate']
            b.files = request.FILES['files'].filename
import hashlib
import os, struct


def encrypt(password, input, path, chunksize = 64*512):
    key = hashlib.sha256(password).digest()
    outfile = input + '.enc'
    iv = ''.join(chr(random.randint(0, 0xFF)) for i in range(16))
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    filesize = os.path.getsize(path+ '\\' +input)
       with open(input, 'rb') as infile:
        with open(outfile, 'wb') as outf:
            outf.write(struct.pack('<Q', filesize))
            outf.write(iv)
            outf.write(key)

            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += ' ' * (16 - len(chunk) % 16)
                outf.write(encryptor.encrypt(chunk))

def decrypt(password, input, chunksize = 16*512):
    output = input[:-4]
    with open(input, 'rb') as infile:
        fsize = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
        iv = infile.read(16)
        check = infile.read(32)
        key = hashlib.sha256(password)
        if(check != key):
            return False
        decryptor = AES.new(key, AES.MODE_CBC, iv)

        with open(output, 'wb') as outfile:
            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                outfile.write(decryptor.decrypt(chunk))

            outfile.truncate(fsize)

    return True




