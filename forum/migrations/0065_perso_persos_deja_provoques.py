# Generated by Django 2.1.3 on 2018-12-11 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0064_auto_20181211_1104'),
    ]

    operations = [
        migrations.AddField(
            model_name='perso',
            name='persos_deja_provoques',
            field=models.ManyToManyField(blank=True, related_name='_perso_persos_deja_provoques_+', to='forum.Perso'),
        ),
    ]