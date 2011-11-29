from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin

#from app.admin_views import admin_autodiscover

admin.autodiscover()
#admin_autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'xml_to_db.app.views.home', name='home'),
    url(r'^admin/', include(admin.site.urls)),
    #url(r'^admin/(?P<app_label>\w+)/(?P<model_name>\w+)/$', 'xml_to_db.app.admin_views.view_new_model'),
    url(r'^admin/(?P<app_label>\w+)/(?P<model_name>\w+)/add/$', 'xml_to_db.app.admin_views.add_item'),
)
