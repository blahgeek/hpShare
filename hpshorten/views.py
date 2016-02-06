# from django.shortcuts import render, redirect
import django.shortcuts
from hashid.models import HashID
from .models import StaticRedirection

# Create your views here.

def redirect(req, id):
    model = HashID.get_related(id, 'hpshorten_redirect')
    return django.shortcuts.redirect(model.url, permanent=model.permanent)

def redirect_static(req, id):
    model = django.shortcuts.get_object_or_404(StaticRedirection, id=id).redirection
    return django.shortcuts.redirect(model.url, permanent=model.permanent)
