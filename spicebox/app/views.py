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

