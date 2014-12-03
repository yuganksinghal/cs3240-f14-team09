from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from app.models import Bulletin, File, User
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django import forms
from app.forms import UserForm, BulletinForm, EditBulletinForm
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, render
from django.db.models import Q
from itertools import chain
import datetime


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

def user_logout(request):
    logout(request)
      
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

def search_Bulletin(request):
    context = {}
    context['month_loop'] = range(1,13)
    context['day_loop'] = range(1,32)
    context['year_loop'] = range(1900, 2015)

    if request.method == 'POST':
        search_text = request.POST['search_text']
        #search_year = request.POST['year']
        #search_month = request.POST['month']
        #search_day = request.POST['day']
        if len(search_text) > 0:
            queryset = Bulletin.objects.all()
            queryset = queryset.filter(Q(description__icontains=search_text) | Q(title__icontains=search_text ))
            context['search_result'] = queryset

            #queryset2 = User.objects.all()
            #queryset2 = queryset2.filter(username__icontains=search_text)

            #queryset3 = Bulletin.objects.all()
            #queryset3 = queryset3.filter(Q(pub_date__year=search_year) | Q(pub_date__month = search_month) | Q(pub_date__day = search_day))

            #allset = list(chain(queryset, queryset3))
            #context['search_result'] = allset

        else:
            context['search_result'] = Bulletin.objects.none()
    return render(request, 'search_bulletin.html', context)

def post_Bulletin(request):
    if(request.method== 'POST'):
        form = BulletinForm(request.POST, request.FILES)
        if form.is_valid():
            print "Creating new Bulletin"
            b = Bulletin()
            f = File()
            b.author = request.user
            b.description = request.POST['description']
            b.pub_date = datetime.datetime.now()
            f.path = request.FILES['path']
            b.save()
            f.bulletin = b
            f.save()
            return HttpResponse("Saved!")

    else:
        form=BulletinForm()

    return render_to_response(
        'AddBulletin.html',
        {'form': form},
        context_instance=RequestContext(request)
    )

def edit_Bulletin(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            pk = request.POST['bulletin']
            bulletin = Bulletin.objects.get(pk=pk)
            bulletin.description = request.POST['description']
	    bulletin.save()
            return HttpResponse("updated")
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
  
    
def delete_Bulletin(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            pk = request.POST['bulletin']
            bulletin = Bulletin.objects.get(pk=pk)
            bulletin.delete()
            return HttpResponse("deleted")
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

      
def copy_Bulletin(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            pk = request.POST['bulletin']
            bulletin = Bulletin.objects.get(pk=pk)
            bulletin_copy = Bulletin(
                description=bulletin.description,
                author=bulletin.author,
                pub_date=bulletin.pub_date
            )
            bulletin_copy.save()
            return HttpResponse("copied")
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
