from django.conf.urls import patterns,url,include
from app import views
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^$',views.default, name='default'),
    url(r'^login/$',views.user_login, name='login'),
    url(r'^bulletins/$',views.bulletins, name='bulletins'),
     url(r'^my_bulletins/$',views.my_bulletins, name='my bulletin'),
    url(r'^my_bulletins/move$',views.move_bulletin, name='move bulletin'),
    url(r'^register/$', views.register, name='register'),
    url(r'^folders/$', views.folders, name='folders'),
    url(r'^folders/add/$',views.add_folder, name='add folder'),
    url(r'^folders/delete/$',views.delete_folder, name='delete folder'),
    url(r'^admin/', include(admin.site.urls)),
)
