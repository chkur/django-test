#-*-encoding:utf-8-*-
from app import models
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db import connection, models
from django.contrib import admin
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.admin import widgets, helpers
from django.forms.models import ModelForm

from views import yaml_models, get_csrf_context


def add_item(request, app_label, model_name):
    yaml_model = models.get_model('app', model_name)

    class YamlForm(ModelForm):
        class Meta:
            model=yaml_model

    if request.method=='GET':
        form = YamlForm()
    else:
        form = YamlForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/admin/%s/%s' % (app_label, model_name))

    return render_to_response('admin/yaml_change_form.html',{
            'form':form,
            'is_popup':False,
            'opts':yaml_model._meta,
            'change':False,
            'save_as':False,
            'has_delete_permission':False,
            'has_add_permission':True,
            'has_change_permission':False,
            'add':True,
                }, get_csrf_context(request),
            )


def edit_item(request, app_label, model_name, id):
    yaml_model = models.get_model('app', model_name)

    class YamlForm(ModelForm):
        class Meta:
            model=yaml_model
            
    instance = yaml_model.objects.get(pk=id)
    print instance
    
    if request.method=='GET':
        form = YamlForm(instance=instance)
    else:
        form = YamlForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/admin/%s/%s' % (app_label, model_name))

    return render_to_response('admin/yaml_change_form.html',{
            'form':form,
            'is_popup':False,
            'opts':yaml_model._meta,
            'change':True,
            'save_as':False,
            'has_delete_permission':False,
            'has_add_permission':True,
            'has_change_permission':False,
            'add':True,
                }, get_csrf_context(request),
            )


def view_model(request, app_label, model_name):
    yaml_model = models.get_model('app', model_name)
    rows = yaml_model.objects.all()

    return render_to_response('admin/yaml_model.html',{
            'rows':rows,
            'model_name':model_name,
            'app_label':app_label,
            'is_popup':False,
            'opts':yaml_model._meta,
            'change':True,
            'save_as':False,
            'has_delete_permission':False,
            'has_add_permission':True,
            'has_change_permission':False,
            'add':True,
                }, get_csrf_context(request),
            )


def delete_item(request, app_label, model_name, id):
    yaml_model = models.get_model('app', model_name)
    item = yaml_model.objects.get(id=id)
    item.delete()
    return HttpResponseRedirect('/admin/%s/%s' % (app_label, model_name))
