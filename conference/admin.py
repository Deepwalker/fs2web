from django.contrib import admin
from models import *

def start_conf(modeladmin, request, queryset):
    for obj in queryset:
        obj.start()
start_conf.short_description = "Start conference"

class ConferenceAdmin(admin.ModelAdmin):
    actions=[start_conf]


admin.site.register(Conference,ConferenceAdmin)
admin.site.register(Phone)

