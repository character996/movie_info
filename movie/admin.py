from django.contrib import admin
from .models import Top250, SearchTitle, SearchResult, SearchRecord
# Register your models here.


class Top250Admin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ('rank', 'worker', 'name')
    # list_filter = ['rank']
    list_per_page = 20


admin.site.register(Top250, Top250Admin)


class SearchResultInline(admin.TabularInline):
    model = SearchResult
    extra = 3


class SearchTitleAdmin(admin.ModelAdmin):
    list_per_page = 10
    inlines = [SearchResultInline]
    list_display = ('title', 'create_date', 'result_count')


@admin.register(SearchRecord)
class SearchRecordAdmin(admin.ModelAdmin):
    list_display = ('title', 'num', 'user', 'result', 'c_time')
    list_filter = ('user__name', 'c_time')
    list_per_page = 15
    list_display_links = None


admin.site.register(SearchTitle, SearchTitleAdmin)
