from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'hpshare.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^permit/', 'hpshare.views.permit', name='permit'), 
    url(r'^callback/', 'hpshare.views.callback', name='callback'),
    url(r'^delete/', 'hpshare.views.deletefile', name='deletefile'),
    url(r'^(?P<id>[0-9a-zA-Z]+)$', 'hpshare.views.viewfile', name='viewfile'),
    url(r'^(?P<id>[0-9a-zA-Z]+)/(?P<filename>[^/]+)$', 'hpshare.views.previewfile', name='previewfile'),
    url(r'^download/(?P<id>[0-9a-zA-Z]+)/(?P<filename>[^/]+)$', 'hpshare.views.downloadfile', name='downloadfile'),
    # url(r'^upload/', 'hpshare.views.upload', name='upload'),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
