from django.http import HttpResponse
from django.template import RequestContext, loader
from app.models import Bulletin
django.contrib.admin.models import User
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
