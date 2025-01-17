# Generated by Django 2.1.1 on 2018-11-03 18:14

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0034_auto_20181103_1419'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='commande',
            name='fonction',
        ),
        migrations.RemoveField(
            model_name='commande',
            name='lieu_cible',
        ),
        migrations.AddField(
            model_name='commande',
            name='lieux_cible',
            field=models.ManyToManyField(blank=True, related_name='lieux_cible', to='forum.Lieu'),
        ),
        migrations.AlterField(
            model_name='commande',
            name='date_validation',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
