from django.contrib import admin
from .models import Top250, SearchTitle
# Register your models here.


class Top250Admin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ('rank', 'worker', 'name')
    # list_filter = ['rank']
    list_per_page = 20


admin.site.register(Top250, Top250Admin)


class SearchTitleAdmin(admin.ModelAdmin):
    list_per_page = 10


admin.site.register(SearchTitle, SearchTitleAdmin)
