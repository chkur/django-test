#-*-encoding:utf-8-*-
import os

import yaml


from django import forms
from django.db import connection, models
from django.template import RequestContext
from django.contrib import admin
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.core.management import sql, color
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required

from settings import PROJECT_ROOT

FIELD_TYPES = { 'int':models.IntegerField,
                'char':models.TextField,
                'bool':models.BooleanField,
                }


yaml_models = {}


def get_csrf_context(request):
    c = {}
    c.update(csrf(request))
    return RequestContext(request, c)


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


def install(model):
    style = color.no_style()
    cursor = connection.cursor()
    statements, pending = connection.creation.sql_create_model(model, style)
    for sql in statements:
        cursor.execute(sql)


def create_yaml_models(request, din_models_yaml):
    for key, value in din_models_yaml.items():
        new_model = create_model(key, app_label='app', 
                                module='xml_to_db.app.models', 
                                fields=dict((i['id'], FIELD_TYPES[i['type']](verbose_name=i['title'])) for i in value['fields']), 
                                options={'verbose_name_plural':value['title']})
        this_model = new_model()
        yaml_models[key] = this_model
    #request.session['yaml_models'] = yaml_models.keys()
    return yaml_models

@login_required
def home(request):

    class yaml_form(forms.Form):
        file_ = forms.FileField(label=u'YAML-файл')
        
    error = None
    if request.method=='GET':
        form = yaml_form()
    else:
        form = yaml_form(request.POST, request.FILES)
        if form.is_valid():
            file_text = request.FILES['file_'].read()
            try:
                din_models_yaml = yaml.load(file_text)
            except:
                return render_to_response('base.html',{
                        'form':form,
                        'error':u'Ошибка формата файла',
                            }, get_csrf_context(request),
                        )
            try:
                myapp = models.get_app('app')
                create_yaml_models(request, din_models_yaml)

                for yaml_model in yaml_models.values():
                    try:
                        install(yaml_model)
                    except:
                        print 'not installed'
            except:
                error = u'Ошибка создания таблицы'

            return HttpResponseRedirect('/admin/app/')
            
    return render_to_response('base.html',{
            'form':form,
            'error':error,
                }, get_csrf_context(request),
            )

            
