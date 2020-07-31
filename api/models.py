# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AllMovie(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=50, blank=True, null=True)
    rate = models.CharField(max_length=5, blank=True, null=True)
    casts = models.CharField(max_length=100, blank=True, null=True)
    url = models.CharField(max_length=50, blank=True, null=True)
    directors = models.CharField(max_length=30, blank=True, null=True)
    cover = models.CharField(max_length=100, blank=True, null=True)
    tags = models.CharField(max_length=30, blank=True, null=True)
    intro = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'all_movie'
        ordering = ('-rate', )


class Director(models.Model):
    name = models.CharField(verbose_name='导演', max_length=20, unique=True)

    class Meta:
        db_table = 'all_directors'

    def __str__(self):
        return self.name


class Actor(models.Model):
    name = models.CharField(verbose_name='演员', max_length=20, unique=True)

    class Meta:
        db_table = 'all_actors'

    def __str__(self):
        return self.name


class Tag(models.Model):
    tag = models.CharField(verbose_name='标签', max_length=10, unique=True)

    class Meta:
        db_table = 'all_tags'

    def __str__(self):
        return self.tag


class AllMovieInfo(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=50, blank=True, null=True)
    rate = models.CharField(max_length=5, blank=True, null=True)
    casts = models.ManyToManyField(Actor)
    url = models.CharField(max_length=50, blank=True, null=True)
    directors = models.ManyToManyField(Director)
    cover = models.CharField(max_length=100, blank=True, null=True)
    tags = models.ManyToManyField(Tag)
    intro = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'all_movie_info'
        ordering = ('id', )

    def __str__(self):

        return self.title, self.id


