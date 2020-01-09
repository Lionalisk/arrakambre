# Generated by Django 2.1.3 on 2019-09-11 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0183_auto_20190911_1658'),
    ]

    operations = [
        migrations.AddField(
            model_name='objet',
            name='cumulable',
            field=models.BooleanField(default=False, verbose_name='cumulable : se compte avec les autres objets identiques (ex:potion)'),
        ),
        migrations.AddField(
            model_name='objet',
            name='reparable',
            field=models.BooleanField(default=False),
        ),
    ]
