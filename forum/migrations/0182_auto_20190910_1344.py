# Generated by Django 2.1.3 on 2019-09-10 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0181_auto_20190910_1018'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='perso',
            name='image',
        ),
        migrations.AddField(
            model_name='perso',
            name='nom_info',
            field=models.CharField(default='perso_none', max_length=40),
        ),
    ]
