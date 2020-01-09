# Generated by Django 2.1.3 on 2019-07-23 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0175_jeu_delai_refresh'),
    ]

    operations = [
        migrations.AddField(
            model_name='jeu',
            name='lock_onload',
            field=models.BooleanField(default=False, verbose_name="param temporaire pour empecher le thread d'onload en même temps qu'un refresh manuel - A LAISSER DECOCHE !"),
        ),
    ]
