from django.contrib import admin
from django.core.urlresolvers import reverse
from django.utils.html import format_html
# Register your models here.

from .models import Redirection, StaticRedirection

@admin.register(Redirection)
class RedirectionAdmin(admin.ModelAdmin):
    list_display = ('hashid', 'link', 'url', 'permanent')
    ordering = ('hashid__create_time', )

    def link(self, obj):
        url = reverse('hpshorten_redirect', args=[obj.hashid.hashid, ])
        return format_html('<a href="{0}">link</a>', url)
    link.allow_tags = True

@admin.register(StaticRedirection)
class StaticRedirectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'redirection', )
