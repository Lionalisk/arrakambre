# Generated by Django 2.1.3 on 2018-12-11 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0063_auto_20181207_1725'),
    ]

    operations = [
        migrations.AddField(
            model_name='perso',
            name='accepte_combat',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='perso',
            name='accepte_duel',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='perso',
            name='aura',
            field=models.SmallIntegerField(default=0),
        ),
    ]
