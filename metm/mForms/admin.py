from django.contrib import admin
from mForms.models import Forms,Fields,Values,SendList

admin.site.register(Fields)
admin.site.register(SendList)

class FieldsForForm(admin.TabularInline):
    model = Fields
    extra = 0
class EmailForForm(admin.TabularInline):
    model = SendList
    extra = 0

@admin.register(Forms)
class AdminForms(admin.ModelAdmin):

    inlines = [FieldsForForm,EmailForForm]
# Register your models here.

class ValuesAdmin(admin.ModelAdmin):
    list_display = ('forms','form_fields','value')
    search_fields= ('forms','form_fields','value')
    list_filter = ('forms','form_fields','value')
    # fields = ('title','category','author','tags','short_description','long_description','image','is_published')
    save_on_top=True
    fieldsets= (
       ('Relations',{
        'description':'Relations',
        'fields':('forms','form_fields',),
        'classes': ('collapse',)
    }),('Information',{
        'description':'Information',
        'fields':('value',),
        'classes':('collapse',)
    }),
    )
admin.site.register(Values,ValuesAdmin)
