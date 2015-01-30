from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'hpshare.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^permit/', 'hpshare.views.permit', name='permit'), 
    url(r'^callback/', 'hpshare.views.callback', name='callback'),
    url(r'^f/(?P<id>[0-9a-zA-Z]+)/(?P<filename>[^/]+)', 'hpshare.views.viewfile', name='viewfile'),
    # url(r'^upload/', 'hpshare.views.upload', name='upload'),
)
