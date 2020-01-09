# Generated by Django 2.1.3 on 2019-11-14 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0224_auto_20191112_1546'),
    ]

    operations = [
        migrations.AddField(
            model_name='posture',
            name='description2',
            field=models.TextField(blank=True, null=True, verbose_name='description2 : se genere automatiquement'),
        ),
        migrations.AddField(
            model_name='posture',
            name='lock_description2',
            field=models.BooleanField(default=False, verbose_name='si oui, description2 ne se genere pas automatiquement'),
        ),
    ]
