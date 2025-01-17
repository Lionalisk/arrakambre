# Generated by Django 2.1.1 on 2018-11-01 09:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0027_auto_20181101_1052'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perso',
            name='lieu',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='localisation', to='forum.Lieu'),
        ),
        migrations.AlterField(
            model_name='perso',
            name='maison',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='forum.Maison'),
        ),
    ]
