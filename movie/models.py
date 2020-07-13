# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Top250(models.Model):
    rank = models.IntegerField(primary_key=True)
    href = models.CharField(max_length=200)
    name = models.CharField(max_length=100)
    worker = models.CharField(max_length=200, blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    score = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'top250'

    def __str__(self):
        return self.name


class Users(models.Model):
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'users'


class SearchTitle(models.Model):
    title = models.CharField(max_length=30, null=False)
    create_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'title'

    def __str__(self):
        return self.title


class SearchResult(models.Model):
    name = models.CharField(max_length=200)
    href = models.CharField(max_length=100)
    workers = models.CharField(max_length=200)
    abstract = models.CharField(max_length=200)
    score = models.CharField(max_length=10)
    title = models.ForeignKey(SearchTitle, on_delete=models.CASCADE)

    class Meta:
        db_table = 'search_result'
