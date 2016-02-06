from django.contrib import admin

# Register your models here.

from .models import HashID

@admin.register(HashID)
class HashIDAdmin(admin.ModelAdmin):
    list_display = ('hashid', 'private', 'enabled',
                    'create_time', 'last_access_time',
                    'view_count', 
                    'hpshare_storage', 'hpshare_converted_storage', 'hpshare_storage_group')
    ordering = ('create_time', )
