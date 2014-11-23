from django.conf.urls import patterns,url
from app import views

urlpatterns = patterns('',
    url(r'^login/$',views.user_login, name='login'),
    url(r'^home/$',views.home, name='home'),
    url(r'^register/$', views.register, name='register'),
    url(r'^add/$', views.post_Bulletin, name='add')

)

