# Generated by Django 2.2.13 on 2020-07-09 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Top250',
            fields=[
                ('rank', models.IntegerField(primary_key=True, serialize=False)),
                ('href', models.CharField(max_length=200)),
                ('name', models.CharField(max_length=100)),
                ('worker', models.CharField(blank=True, max_length=200, null=True)),
                ('category', models.CharField(blank=True, max_length=100, null=True)),
                ('score', models.FloatField(blank=True, null=True)),
            ],
            options={
                'managed': False,
                'db_table': 'top250',
            },
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=255)),
                ('password', models.CharField(max_length=255)),
            ],
            options={
                'managed': False,
                'db_table': 'users',
            },
        ),
    ]
