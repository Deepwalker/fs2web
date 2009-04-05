from django.contrib import admin
from models import *

#class VarInline(admin.TabularInline):
#    model = Agent 
#    extra = 3
#
#class FSGAdmin(admin.ModelAdmin):
#    inlines = [VarInline]
#
#admin.site.register(HuntGroup,FSGAdmin)

class ExtInline(admin.TabularInline):
    model = Extension
    extra = 5
    template = "condition_inline.html"
class CondInline(admin.TabularInline):
    model = Condition
    extra = 3
    template = "condition_inline.html"
class ActInline(admin.TabularInline):
    model = Action
    extra = 10

class Cont_Admin(admin.ModelAdmin):
    inlines = [ExtInline]
class Ext_Admin(admin.ModelAdmin):
    inlines = [CondInline]
class Cond_Admin(admin.ModelAdmin):
    inlines = [ActInline]

admin.site.register(Extension, Ext_Admin)
admin.site.register(Condition, Cond_Admin)
admin.site.register(Context,Cont_Admin)

admin.site.register(DPApp)

