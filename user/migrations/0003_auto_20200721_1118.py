# Generated by Django 2.2.13 on 2020-07-21 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20200721_0957'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='confirmstring',
            options={'ordering': ['-c_time'], 'verbose_name': '确认码', 'verbose_name_plural': '确认码'},
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254),
        ),
    ]
