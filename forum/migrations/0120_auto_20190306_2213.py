# Generated by Django 2.1.1 on 2019-03-06 21:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0119_auto_20190306_1507'),
    ]

    operations = [
        migrations.AddField(
            model_name='action',
            name='condition_cible_possible',
            field=models.BooleanField(default=False, verbose_name='OK seulement si au moins une cible est possible'),
        ),
        migrations.AlterField(
            model_name='action',
            name='cibleperso_cache',
            field=models.SmallIntegerField(choices=[(0, 'La cible peut être caché ou non'), (1, 'La cible ne doit pas être cachée, même si repéré par joueur'), (2, 'La cible doit être cachée, même si repérée par joueur')], default=0, verbose_name='Cible Perso : est caché ?'),
        ),
    ]
