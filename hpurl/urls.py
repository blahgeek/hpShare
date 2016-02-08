from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'hpshare.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url('^$', RedirectView.as_view(url='/~admin/', permanent=False), name='index_redirect'),
    url(r'^~cli/hpshare/?$', RedirectView.as_view(url='/~static/clients/bash/hpshare.bash', permanent=False)),
    url(r'^~admin/', include(admin.site.urls)),

    # hpShare
    url(r'^~api/hpshare/', include('hpshare.apis', 'hpshare_api')),
    url(r'^F', include('hpshare.views', 'hpshare')),
    url(r'^G(?P<id>[0-9a-zA-Z]+)/?$', 'hpshare.views.viewgroup', name='hpshare_viewgroup'),

    # hpShorten
    url(r'^R(?P<id>[0-9a-zA-Z]+)/?$', 'hpshorten.views.redirect', name='hpshorten_redirect'),

    # fallback to static redirect
    url(r'^(?P<id>[0-9a-zA-Z]+)/?$', 'hpshorten.views.redirect_static', name='hpshorten_redirect_static'),

) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
