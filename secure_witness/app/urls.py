from django.conf.urls import patterns,url,include
from app import views
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('',
    url(r'^$',views.default, name='default'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$',views.user_login, name='login'),
    url(r'^logout/$',views.user_logout, name='logout'),
    url(r'^bulletins/$',views.bulletins, name='bulletins'),
    url(r'^bulletins/search/$', views.search_Bulletin, name='search bulletin'), 
    url(r'^my_bulletins/$',views.my_bulletins, name='my bulletins'),
    url(r'^bulletins/chart/$',views.bulletins_chart, name='bulletins chart'),
    url(r'^my_bulletins/chart/$',views.my_bulletins_chart, name='my bulletins chart'),
    url(r'^my_bulletins/move/$',views.move_bulletin, name='move bulletin'),
    url(r'^my_bulletins/add/$',views.add_bulletin, name='add bulletin'),
    url(r'^my_bulletins/edit/$', views.edit_bulletin, name='edit bulletin'),
    url(r'^my_bulletins/copy/$', views.copy_bulletin, name='copy bulletin'),
    url(r'^my_bulletins/delete/$', views.delete_bulletin, name='delete bulletin'),
    url(r'^folders/$', views.folders, name='folders'),
    url(r'^folders/add/$',views.add_folder, name='add folder'),
    url(r'^folders/delete/$',views.delete_folder, name='delete folder'),
    url(r'^folders/copy/$',views.copy_folder, name='copy folder'),
    url(r'^folders/rename/$',views.rename_folder, name='rename folder'),
    url(r'^files/(?P<file_id>\d+)/$', views.get_file, name='get file'),
    #url(r'^files/add/$', views.add_file, name='add file'),
    url(r'^admin/', include(admin.site.urls)),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
