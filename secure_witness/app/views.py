from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django import forms
from app.forms import UserForm, BulletinForm
from django.core.urlresolvers import reverse
from app.models import Bulletin, Folder, File
from django.shortcuts import render_to_response
import datetime 
from encryption import encrypt_file, decrypt_file
import os
from django.conf import settings

def default(request):
    return HttpResponseRedirect(reverse('bulletins'))

def register(request):
    registered = False
    if request.method =='POST':
        user_form = UserForm(data=request.POST)
        print request.POST

        if user_form.is_valid():
            user = user_form.save()            
            user.set_password(user.password)
            user.save()
            folder = Folder(name=user.username, owner=user)
            folder.save()
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
        return HttpResponseRedirect(reverse('logi+n'))
            
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

def copy_folder(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            pk = request.POST['folder']
            folder = Folder.objects.get(pk=pk)
            folder_copy = Folder(
                name=folder.name +"_copy",
                owner=folder.owner
            )
            folder_copy.save()
            for bulletin in folder.bulletin_set.all():
                folder_copy.bulletin_set.create(
                    title=bulletin.title,
                    description=bulletin.description,
                    pub_date=bulletin.pub_date,
                    author=bulletin.author,
                    folder=bulletin.folder
                )
            return HttpResponseRedirect(reverse('folders'))
        else:
            user = request.user
            folders = user.folder_set.all()
            template = loader.get_template('copy_folder.djhtml')
            context = RequestContext(request,{
                'user': user, 
                'folders': folders
            })
            return HttpResponse(template.render(context))
    else:
         return HttpResponseRedirect(reverse('login'))

def rename_folder(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            folder_pk = request.POST['folder_pk']
            name = request.POST['name']
            folder = Folder.objects.get(pk=folder_pk)
            folder.name = name
            folder.save()
            return HttpResponseRedirect(reverse('folders'))
        else:
            user = request.user
            folders = user.folder_set.all()
            template = loader.get_template('rename_folder.djhtml')
            context = RequestContext(request,{
                'folders': folders,
            })
            return HttpResponse(template.render(context))
    else:
        return HttpResponseRedirect(reverse('login'))

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

def bulletins_chart(request):
    if request.user.is_authenticated():
        bulletins = Bulletin.objects.order_by('-pub_date')
        files = []
        for bulletin in bulletins:
            files.extend(bulletin.file_set.all())
        template = loader.get_template('bulletins_chart.djhtml')
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


def my_bulletins_chart(request):
    if request.user.is_authenticated():
        user = request.user
        bulletins = user.bulletin_set.order_by('-pub_date')
        files = []
        for bulletin in bulletins:
            files.extend(bulletin.file_set.all())
            template = loader.get_template('my_bulletins_chart.djhtml')
            context = RequestContext(request, {
            'bulletins':bulletins,
            'files':files
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

def add_bulletin(request):
    if request.user.is_authenticated():
        if(request.method== 'POST'):
            form = BulletinForm(request.POST, request.FILES)
            if form.is_valid():
                title = request.POST['title']
                description = request.POST['description']
                pub_date = datetime.datetime.now()
                author = request.user
                folder = Folder.objects.get(name=str(author))
                bulletin = Bulletin(
                    title=title, 
                    description=description,
                    pub_date = pub_date,
                    author = author,
                    folder = folder
                )
                if request.POST.get('anonymous'):
                     bulletin.anonymous = True
                bulletin.save()
                for filename, file in request.FILES.iteritems():
                    path =settings.MEDIA_ROOT+'/'+request.user.username+'/'+request.FILES[filename].name
                    if os.path.exists(path):
                        os.remove(path)
                    bulletin.file_set.create(
                    filename = request.FILES[filename].name,
                    path = file,
                    user = author
                    )
                password = request.POST['password']
                for file in bulletin.file_set.all():
                    path = os.getcwd() + file.path.url
                    encrypt_file(password, path)
                    os.remove(path)
                    decrypt_file(password,path+".enc")
                return HttpResponseRedirect(reverse('my bulletins'))

        else:
            form=BulletinForm()
            return render_to_response(
            'add_bulletin.djhtml',
                {'form': form},
                context_instance=RequestContext(request)
            )
    else:
        return HttpResponseRedirect(reverse('login'))

def edit_bulletin(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            pk = request.POST['bulletin']
            bulletin = Bulletin.objects.get(pk=pk)
            bulletin.description = request.POST['description']
	    bulletin.save()
            return HttpResponseRedirect(reverse('my bulletins'))
        else:
            user = request.user
            bulletins = user.bulletin_set.all()
            template = loader.get_template('edit_bulletin.djhtml')
            context = RequestContext(request,{
                'user': user, 
                'bulletins': bulletins
            })
            return HttpResponse(template.render(context))
    else:
         return HttpResponseRedirect(reverse('login'))
  
    
def delete_bulletin(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            pk = request.POST['bulletin']
            bulletin = Bulletin.objects.get(pk=pk)
            bulletin.delete()
            return HttpResponseRedirect(reverse('my bulletins'))
        else:
            user = request.user
            bulletins = user.bulletin_set.all()
            template = loader.get_template('delete_bulletin.djhtml')
            context = RequestContext(request,{
                'user': user, 
                'bulletins': bulletins
            })
            return HttpResponse(template.render(context))
    else:
         return HttpResponseRedirect('login')

def copy_bulletin(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            pk = request.POST['bulletin']
            bulletin = Bulletin.objects.get(pk=pk)
            bulletin_copy = Bulletin(
                title=bulletin.title+"_copy",
                description=bulletin.description,
                pub_date=bulletin.pub_date,
                author=bulletin.author,
                folder=bulletin.folder
            )
            bulletin_copy.save()
            for file in bulletin_copy.file_set.all():
                folder_copy.bulletin_set.create(
                    filename=file.filename,
                    path=file.path,
                    user=file.user
                )
            return HttpResponseRedirect(reverse('my bulletins'))
        else:
            user = request.user
            bulletins = user.bulletin_set.all()
            template = loader.get_template('copy_bulletin.djhtml')
            context = RequestContext(request,{
                'user': user, 
                'bulletins': bulletins
            })
            return HttpResponse(template.render(context))
    else:
         return HttpResponseRedirect(reverse('login'))
