from django.contrib import admin
from .models import AllMovieInfo, Actor, Director, Tag
# Register your models here.

admin.site.register(AllMovieInfo)
admin.site.register(Tag)
admin.site.register(Actor)
admin.site.register(Director)
