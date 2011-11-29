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


# ACTION_CHECKBOX_NAME is unused, but should stay since its import from here
# has been referenced in documentation.
from django.contrib.admin.helpers import ACTION_CHECKBOX_NAME
from django.contrib.admin.options import ModelAdmin, HORIZONTAL, VERTICAL
from django.contrib.admin.options import StackedInline, TabularInline
from django.contrib.admin.sites import AdminSite

def view_new_model(request, app_label, model_name):
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
            'change':False,
            'is_popup':False,
            'save_as':False,
            'has_delete_permission':False,
            'has_add_permission':True,
            'has_change_permission':False,
            'add':True,
                }, RequestContext(request, c),
            )


class YamlModelAdmin(ModelAdmin):
    #def __init__(self, *args, **kwargs):
        #super(ModelAdmin, self).__init__()
    def __init__(self, model, admin_site):
        super(ModelAdmin, self).__init__()
        self.model = yaml_models[model]



class YamlAdminSite(AdminSite):
    def __init__(self, *args, **kwargs):
        super(AdminSite, self).__init__()
        self._registry = yaml_models
        print '!!!!!!!!!!!', self._registry, yaml_models
        #self.model = yaml_models[0]



site = YamlAdminSite()


def admin_autodiscover():
    """
    Auto-discover INSTALLED_APPS admin.py modules and fail silently when
    not present. This forces an import on them to register any admin bits they
    may want.
    """
    import copy
    from django.conf import settings
    from django.utils.importlib import import_module
    from django.utils.module_loading import module_has_submodule

    for app in settings.INSTALLED_APPS:
        mod = import_module(app)
        # Attempt to import the app's admin module.
        try:
            before_import_registry = copy.copy(site._registry)
            import_module('%s.admin' % app)
        except:
            # Reset the model registry to the state before the last import as
            # this import will have to reoccur on the next request and this
            # could raise NotRegistered and AlreadyRegistered exceptions
            # (see #8245).
            site._registry = before_import_registry

            # Decide whether to bubble up this error. If the app just
            # doesn't have an admin module, we can ignore the error
            # attempting to import it, otherwise we want it to bubble up.
            if module_has_submodule(mod, 'admin'):
                raise
