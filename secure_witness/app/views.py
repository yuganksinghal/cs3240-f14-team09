from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django import forms
from app.forms import UserForm
from django.core.urlresolvers import reverse
from app.models import Bulletin, Folder, File

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
            return HttpResponseRedirect(reverse('bulletins'))
        else:
            return HttpResponse("Invalid login credentials supplied")
    else:
        template = loader.get_template('login.djhtml')
        context = RequestContext(request)
        return HttpResponse(template.render(context))

def default(request):
    return HttpResponseRedirect(reverse('bulletins'))

def bulletins(request):
    if request.user.is_authenticated():
        bulletins = Bulletin.objects.order_by('-pub_date')
        files = []
        for bulletin in bulletins:
            files.extend(bulletin.file_set.all())
        template = loader.get_template('bulletins.djhtml')
        context = RequestContext(request, {
        'bulletins':bulletins,
        'files':files
        })
        return HttpResponse(template.render(context))
    else:
        return HttpResponseRedirect(reverse('login'))

def my_bulletins(request):
    if request.user.is_authenticated():
        user = request.user
        bulletins = user.bulletin_set.order_by('-pub_date')
        files = []
        for bulletin in bulletins:
            files.extend(bulletin.file_set.all())
            template = loader.get_template('my_bulletins.djhtml')
            context = RequestContext(request, {
            'bulletins':bulletins,
            'files':files
            })
        return HttpResponse(template.render(context))
    else:
        return HttpResponseRedirect(reverse('login'))

def folders(request):
    if request.user.is_authenticated():
        user = request.user
        folders = user.folder_set.all()
        bulletins = []
        for folder in folders:
            bulletins.extend(folder.bulletin_set.all())
                
        template = loader.get_template('folders.djhtml')
        context = RequestContext(request, {
        'user':user,
        'folders':folders,
        'bulletins':bulletins
        })
        return HttpResponse(template.render(context))
    else:
        return HttpResponseRedirect(reverse('login'))
        
def add_folder(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            name = request.POST['name']
            user = request.user
            folder = Folder(name=name, owner=user)
            folder.save()
            return HttpResponseRedirect(reverse('folders'))
            
        else:
            template = loader.get_template('add_folder.djhtml')
            context = RequestContext(request)
            return HttpResponse(template.render(context))
    else:
        return HttpResponseRedirect(reverse('login'))
            
def delete_folder(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            pk = request.POST['folder']
            folder = Folder.objects.get(pk=pk)
            for bulletin in folder.bulletin_set.all():
                bulletin.delete()
                folder.delete()
                return HttpResponseRedirect(reverse('folders'))
            else:
                user = request.user
                folders = user.folder_set.all()
                template = loader.get_template('delete_folder.djhtml')
                context = RequestContext(request,{
                    'user': user, 
                    'folders': folders
                })
                return HttpResponse(template.render(context))
    else:
         return HttpResponseRedirect(reverse('login'))

def move_bulletin(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            bulletin_pk = request.POST['bulletin']
            folder_pk = request.POST['to_folder']
            bulletin = Bulletin.objects.get(pk=bulletin_pk)
            folder = Folder.objects.get(pk=folder_pk)
            bulletin.folder = folder
            bulletin.save()
            return HttpResponseRedirect(reverse('folders'))
        else:
            user = request.user
            folders = user.folder_set.all()
            bulletins = user.bulletin_set.all()
            template = loader.get_template('move_bulletin.djhtml')
            context = RequestContext(request,{
                'folders': folders,
                'bulletins': bulletins
            })
            return HttpResponse(template.render(context))
    else:
        return HttpResponseRedirect(reverse('login'))
   
