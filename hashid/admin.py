from django.contrib import admin

# Register your models here.

from .models import HashID

@admin.register(HashID)
class HashIDAdmin(admin.ModelAdmin):
    list_display = ('id', 'private', 'hashid', 
                    'create_time', 'last_access_time',
                    'view_count')
    ordering = ('create_time', )
