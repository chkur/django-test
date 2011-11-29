from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin

from xml_to_db.app import views, admin_views

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'xml_to_db.app.views.home', name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/(?P<app_label>\w+)/(?P<model_name>\w+)/$', admin_views.view_model, name='view_model'),
    url(r'^admin/(?P<app_label>\w+)/(?P<model_name>\w+)/add/$', admin_views.add_item, name='add_item'),
    url(r'^admin/edit_item/(?P<app_label>\w+)/(?P<model_name>\w+)/(?P<id>\d{1,5})/$', admin_views.edit_item, name='edit_item'),
    url(r'^admin/delete_item/(?P<app_label>\w+)/(?P<model_name>\w+)/(?P<id>\d{1,5})/$', admin_views.delete_item, name='delete_item'),
    url(r'^accounts/login/$',   'django.contrib.auth.views.login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.login'),

)
