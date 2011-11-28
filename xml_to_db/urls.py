from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'xml_to_db.app.views.home', name='home'),
    #url(^'admin/(?P<content_type_id>\d+)/(?P<object_id>.+)/$', some_view)
    url(r'^admin/', include(admin.site.urls)),
)
