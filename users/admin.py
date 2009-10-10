from django.contrib import admin
from models import *

class VarInline(admin.TabularInline):
    model = FSUVariable
    extra = 3

class FSUAdmin(admin.ModelAdmin):
    inlines = [VarInline]


admin.site.register(Variable)
admin.site.register(FSUser,FSUAdmin)
admin.site.register(FSGroup)
admin.site.register(FSDomain)

admin.site.register(gateway)
