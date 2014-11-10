from django.conf.urls import patterns,url
from app import views

urlpatterns = pattern('',
                      url(r'^$',views.login, name='login'),
                      #url(r'^home/$',views.home, name='home'),
)
