# Generated by Django 2.1.1 on 2018-09-22 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0009_auto_20180922_1430'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perso',
            name='Objets',
            field=models.ManyToManyField(blank=True, related_name='objets', to='forum.Objet'),
        ),
        migrations.AlterField(
            model_name='perso',
            name='en_main',
            field=models.ManyToManyField(blank=True, related_name='en_main', to='forum.Objet'),
        ),
    ]
