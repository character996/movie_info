# Generated by Django 2.2.13 on 2020-07-10 09:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SearchTitle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('create_date', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'title',
            },
        ),
        migrations.CreateModel(
            name='SearchResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('href', models.CharField(max_length=100)),
                ('workers', models.CharField(max_length=200)),
                ('abstract', models.CharField(max_length=200)),
                ('score', models.CharField(max_length=10)),
                ('title', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movie.SearchTitle')),
            ],
            options={
                'db_table': 'search_result',
            },
        ),
    ]