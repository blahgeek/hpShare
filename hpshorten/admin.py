from django.contrib import admin

# Register your models here.

from .models import Redirection, StaticRedirection

@admin.register(Redirection)
class RedirectionAdmin(admin.ModelAdmin):
    ordering = ('hashid__create_time', )

@admin.register(StaticRedirection)
class StaticRedirectionAdmin(admin.ModelAdmin):
    pass
