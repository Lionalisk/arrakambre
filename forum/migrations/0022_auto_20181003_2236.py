# Generated by Django 2.1.1 on 2018-10-03 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0021_joueur_maison'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lieu',
            old_name='defense_garde',
            new_name='nbgarde',
        ),
        migrations.AddField(
            model_name='lieu',
            name='nbtroupe',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='lieu',
            name='piege',
            field=models.PositiveIntegerField(default=0),
        ),
    ]