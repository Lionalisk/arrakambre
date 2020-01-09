# Generated by Django 2.1.1 on 2018-11-03 09:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0032_perso_espece'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='perso',
            name='actions_possibles',
        ),
        migrations.RemoveField(
            model_name='perso',
            name='perso_accompagnants',
        ),
        migrations.RemoveField(
            model_name='perso',
            name='perso_prisonnier',
        ),
        migrations.AddField(
            model_name='lieu',
            name='ferme',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='lieu',
            name='inconnu',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='lieu',
            name='nbgarde_max',
            field=models.SmallIntegerField(default=8),
        ),
        migrations.AddField(
            model_name='lieu',
            name='nbtroupe_max',
            field=models.SmallIntegerField(default=8),
        ),
        migrations.AddField(
            model_name='perso',
            name='geolier',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='perso_prisonnier', to='forum.Perso', verbose_name='De qui le perso est prisonnier'),
        ),
        migrations.AddField(
            model_name='perso',
            name='leader',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='perso_accompagne', to='forum.Perso', verbose_name='Qui le perso est en train de suivre'),
        ),
    ]