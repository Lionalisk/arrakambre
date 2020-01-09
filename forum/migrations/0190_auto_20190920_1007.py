# Generated by Django 2.1.3 on 2019-09-20 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0189_auto_20190920_0959'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='objet',
            name='arme_OK',
        ),
        migrations.RemoveField(
            model_name='objet',
            name='armure_OK',
        ),
        migrations.AlterField(
            model_name='objet',
            name='delay',
            field=models.SmallIntegerField(default=0, verbose_name="Delai : duree de l'effet en heure ; pour arme = valeur d'initiative en %"),
        ),
        migrations.AlterField(
            model_name='objet',
            name='valeur3',
            field=models.SmallIntegerField(default=0, verbose_name="valeur3 ; pour arme s'agit du bonus/malus pour dommage"),
        ),
    ]