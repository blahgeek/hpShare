from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.views.generic import RedirectView, TemplateView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'hpshare.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url('^$', RedirectView.as_view(url='~admin/hpshare/storage/', permanent=False), name='index_redirect'),
    url(r'^~cli/?$', RedirectView.as_view(url='~static/clients/bash/hpshare.bash', permanent=False)),
    # APIs
    url(r'^~admin/', include(admin.site.urls)),
    url(r'^~api/permit/', 'hpshare.apis.permit', name='permit'), 
    url(r'^~api/newgroup/', 'hpshare.apis.newgroup', name='newgroup'), 
    url(r'^~api/callback/', 'hpshare.apis.callback', name='callback'),
    url(r'^~api/p-callback/', 'hpshare.apis.persistent_callback', name='persistent_callback'),
    url(r'^~api/delete/', 'hpshare.apis.deletefile', name='deletefile'),

    # Debug :P
    url(r'^~404$', TemplateView.as_view(template_name='404.html')),

    # Views
    url(r'^(?P<id>[0-9a-zA-Z]+)/?$', 'hpshare.views.viewfile', name='viewfile'),
    url(r'^_(?P<id>[0-9a-zA-Z]+)/?$', 'hpshare.views.viewfile', {'disable_preview': True}),
    url(r'^(?P<id>[0-9a-zA-Z]+)_/?$', 'hpshare.views.viewfile', {'disable_preview': True}),

    url(r'^(?P<id>[0-9a-zA-Z]+)/download/?$', 'hpshare.views.downloadfile'),
    url(r'^(?P<id>[0-9a-zA-Z]+)/download/(?P<filename>[^/]+)$', 
        'hpshare.views.downloadfile', 
        name='downloadfile'),
    url(r'^(?P<id>[0-9a-zA-Z]+)/download2/(?P<filename>[^/]+)$', 
        'hpshare.views.downloadfile_persistent', 
        name='downloadfile_persistent'),

    url(r'^g/(?P<id>[0-9a-zA-Z]+)/?$', 'hpshare.views.viewgroup', name='viewgroup'),

) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
