# Generated by Django 2.1.3 on 2019-07-23 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0174_remove_perso_info_signature'),
    ]

    operations = [
        migrations.AddField(
            model_name='jeu',
            name='delai_refresh',
            field=models.SmallIntegerField(default=0, verbose_name='Delai entre chaque rafrachissement automatique, en minute'),
        ),
    ]