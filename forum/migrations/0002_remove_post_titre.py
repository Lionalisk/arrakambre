# Generated by Django 2.1.1 on 2018-09-09 18:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='titre',
        ),
    ]
