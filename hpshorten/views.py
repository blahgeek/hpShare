from django.shortcuts import render, get_object_or_404
import django.shortcuts
from hashid.models import HashID
from .models import StaticRedirection

# Create your views here.

def do_redirect(req, model):
    data = {'url': model.url, 'title': model.title}
    if model.cloak:
        return render(req, 'cloak.html', data)
    else:
        resp = render(req, 'redirect.html', data,
                      status=301 if model.permanent else 302)
        resp['Location'] = model.url
        return resp

def redirect(req, id):
    return do_redirect(req, HashID.get_related(id, 'hpshorten_redirect'))

def redirect_static(req, id):
    return do_redirect(req, get_object_or_404(StaticRedirection, id=id).redirection)
