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
from django.core.context_processors import csrf

from views import yaml_models


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
            return HttpResponseRedirect('/admin/app/')

    c = {}
    c.update(csrf(request))

    return render_to_response('admin/yaml_change_form.html',{
            'form':form,
            'opts':yaml_model._meta,
            'change':True,
            'save_as':False,
            'has_delete_permission':False,
            'has_add_permission':True,
            'has_change_permission':False,
            'add':True,
                }, RequestContext(request, c),
            )
