# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from user.models import User


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
        verbose_name = 'TOP250'
        verbose_name_plural = 'TOP250'

    def __str__(self):
        return self.name


class SearchTitle(models.Model):
    title = models.CharField(max_length=30, null=False)
    create_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'title'
        verbose_name = '搜索标题'
        verbose_name_plural = '搜索标题'

    def __str__(self):
        return self.title

    @property
    def result_count(self):
        return self.searchresult_set.all().count()


class SearchResult(models.Model):
    name = models.CharField(max_length=200)
    href = models.CharField(max_length=100)
    workers = models.CharField(max_length=200)
    abstract = models.CharField(max_length=200)
    score = models.CharField(max_length=10)
    title = models.ForeignKey(SearchTitle, on_delete=models.CASCADE)

    class Meta:
        db_table = 'search_result'


class SearchRecord(models.Model):
    title = models.CharField(max_length=30, verbose_name='搜寻关键字')
    c_time = models.DateTimeField(auto_now_add=True, verbose_name='时间')
    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='用户')
    result = models.BooleanField('查询是否成功')
    num = models.CharField(max_length=3, verbose_name='查询的数量')

    def __str__(self):
        return self.user.name + ':' + self.title

    class Meta:
        db_table = 'search_record'
        verbose_name = '搜索记录'
        verbose_name_plural = '搜索记录'

