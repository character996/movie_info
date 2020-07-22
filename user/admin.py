from django.contrib import admin
from . import models
# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')


admin.site.register(models.User, UserAdmin)
admin.site.register(models.ConfirmString)