from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from app.models import Bulletin, File
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django import forms
from app.forms import UserForm, BulletinForm
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response

def register(request):
    registered = False
    if request.method =='POST':
        user_form = UserForm(data=request.POST)
        print request.POST

        if user_form.is_valid():
            user = user_form.save()            
            user.set_password(user.password)
            user.save()
            registered = True
        else:
            print user_form.errors
    
    else:
        user_form = UserForm()

    template = loader.get_template('register.djhtml')
    context = RequestContext(request, {
        'user_form':user_form,
        'registered':registered
    })
    return HttpResponse(template.render(context))
    
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('home'))
        else:
            return HttpResponse("Invalid login credentials supplied")
    else:
        template = loader.get_template('login.djhtml')
        context = RequestContext(request)
        return HttpResponse(template.render(context))
      
def home(request):
    bulletins = Bulletin.objects.order_by('-pub_date')
    files = []
    for f in bulletins:
        files.extend(f.file_set.all())
    template = loader.get_template('home.djhtml')
    context = RequestContext(request, {
        'bulletins':bulletins,
        'files':files
    })
    return HttpResponse(template.render(context))

def post_Bulletin(request):
    if(request.method== 'POST'):
        form = BulletinForm(request.POST, request.FILES)
        if form.is_valid():
            print "hello"
            b = Bulletin()
            f = File()
            #b.author = request.POST['author']
            b.description = request.POST['description']
            #b.pub_date = request.POST['publication date']
            f.path = request.FILES['path']
            f.save()
            return HttpResponse("Saved!")

    else:
        form=BulletinForm()

    return render_to_response(
        'AddBulletin.html',
        {'form': form},
        context_instance=RequestContext(request)
    )