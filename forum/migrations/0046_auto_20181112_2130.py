# Generated by Django 2.1.1 on 2018-11-12 20:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0045_remove_commande_lieu'),
    ]

    operations = [
        migrations.AlterField(
            model_name='action',
            name='delay',
            field=models.SmallIntegerField(default=100, verbose_name="temps pour réaliser l'action en %"),
        ),
        migrations.AlterField(
            model_name='lieu',
            name='lieu_parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='forum.Lieu', verbose_name='Lieu parent'),
        ),
    ]
