from django.contrib import admin

# Register your models here.
from .models import Catalog, Element

class CatalogAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_title', 'version', 'start_date')
    list_filter = ('full_title','start_date')
    search_fields = ("id", "full_title", "version", "start_date")

class ElementAdmin(admin.ModelAdmin):
    list_display = ('id', 'catalog', 'parent_id', 'code', 'value')
    list_filter = ('catalog','code')
    search_fields = ('id', 'parent_id', 'code', 'value')




admin.site.register(Catalog, CatalogAdmin)
admin.site.register(Element, ElementAdmin)