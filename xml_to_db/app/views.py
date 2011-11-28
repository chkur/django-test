#-*-encoding:utf-8-*-
import os

import yaml

from django.contrib import admin
from django.db import models
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.conf.urls.defaults import patterns
from django.contrib.contenttypes.models import ContentType
from django.db.models.loading import cache 

from xml_to_db import urls as app_urls
from settings import PROJECT_ROOT

FIELD_TYPES = {'int':models.IntegerField(), 'char':models.CharField(max_length=255)}


def create_model(name, fields=None, app_label='', module='', options=None, admin_opts=None):
    """
    Create specified model. Taken from https://code.djangoproject.com/wiki/DynamicModels
    """
    class Meta:
        # Using type('Meta', ...) gives a dictproxy error during model creation
        pass

    if app_label:
        # app_label must be set using the Meta inner class
        setattr(Meta, 'app_label', app_label)

    # Update Meta with any options that were provided
    if options is not None:
        for key, value in options.iteritems():
            setattr(Meta, key, value)

    # Set up a dictionary to simulate declarations within a class
    attrs = {'__module__': module, 'Meta': Meta}

    # Add in any fields that were provided
    if fields:
        attrs.update(fields)

    # Create the class, which automatically triggers ModelBase processing
    model = type(name, (models.Model,), attrs)

    # Create an Admin class if admin options were provided
    #if admin_opts is not None:
        #class Admin(admin.ModelAdmin):
            #pass
        #for key, value in admin_opts:
            #setattr(Admin, key, value)
            #admin.site.register(model, Admin)
    try:
        admin.site.register(model)
    except:
        pass

    return model

#def add_url(url):
    #if hasattr(app_urls,'urlpatterns'):
        #urls = getattr(app_urls,'urlpatterns')
        #urls += patterns('',
            #(r'^admin/app/$', home)
            #(r'^admin/app/(?P<object_id>.+)/$', home)
            #(r'^admin/(?P<path>.*)$', home ),
        #)
        #print urls


def install(model):
    from django.core.management import sql, color
    from django.db import connection

    style = color.no_style()

    cursor = connection.cursor()
    statements, pending = connection.creation.sql_create_model(model, style)
    print statements, pending
    for sql in statements:
        cursor.execute(sql)

def home(request):
    din_models_yaml = yaml.load(open(os.path.join(PROJECT_ROOT,'db','init.ya')).read())
    myapp = models.get_app('app')

    for key, value in din_models_yaml.items():
        new_model = create_model(key, app_label='app', 
                                module='xml_to_db.app.models', 
                                fields=dict((i['id'], FIELD_TYPES[i['type']]) for i in value['fields']), 
                                options={'verbose_name_plural':value['title']})
        this_model = new_model()
        
        try:
            install(this_model)
        except:
            print 'not installed'
    
    return HttpResponseRedirect('/admin/app/')
