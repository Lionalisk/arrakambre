# Generated by Django 2.1.3 on 2019-07-01 15:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0153_auto_20190701_1559'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='perso',
            name='attaque_duel',
        ),
        migrations.RemoveField(
            model_name='perso',
            name='attaque_melee',
        ),
        migrations.RemoveField(
            model_name='perso',
            name='defense_duel',
        ),
        migrations.RemoveField(
            model_name='perso',
            name='defense_melee',
        ),
        migrations.RemoveField(
            model_name='perso',
            name='initiative',
        ),
    ]