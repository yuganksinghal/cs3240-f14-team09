from django.conf.urls import patterns,url
from app import views

urlpatterns = patterns('',
    url(r'^login/$',views.user_login, name='login'),
    url(r'^home/$',views.home, name='home'),
    url(r'^register/$', views.register, name='register'),
    url(r'^bulletin/add/$', views.post_Bulletin, name='add bulletin'),
    url(r'^bulletin/edit/$', views.edit_Bulletin, name='edit bulletin'),
    url(r'^bulletin/copy/$', views.copy_Bulletin, name='copy bulletin'),
    url(r'^bulletin/delete/$', views.delete_Bulletin, name='delete bulletin')

)

