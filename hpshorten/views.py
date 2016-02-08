from django.shortcuts import render, get_object_or_404
import django.shortcuts
from hashid.models import HashID
from .models import StaticRedirection

# Create your views here.

def do_redirect(req, model):
    if model.cloak:
        return render(req, 'cloak.html', {
                        'url': model.url,
                        'title': model.title,
                      })
    return django.shortcuts.redirect(model.url, permanent=model.permanent)

def redirect(req, id):
    return do_redirect(req, HashID.get_related(id, 'hpshorten_redirect'))

def redirect_static(req, id):
    return do_redirect(req, get_object_or_404(StaticRedirection, id=id).redirection)
