# Generated by Django 2.1.3 on 2019-02-22 17:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0108_auto_20190222_1552'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='info_MJ',
        ),
    ]