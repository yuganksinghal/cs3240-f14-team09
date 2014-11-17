from django.conf.urls import patterns,url
from app import views

urlpatterns = patterns('',
                       url(r'^login/$',views.login, name='login'),
                       url(r'^home/$',views.home, name='home')
)
