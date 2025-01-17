# Generated by Django 2.1.3 on 2019-06-06 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0136_post_lock'),
    ]

    operations = [
        migrations.AlterField(
            model_name='action',
            name='cibleperso_est_accompagnant',
            field=models.SmallIntegerField(choices=[(0, 'La cible peut accompagner un autre perso ou non'), (1, "La cible ne doit pas être en train d'accompagner un autre perso"), (2, "La cible doit être en train d'accompagner un autre perso"), (3, "La cible ne doit pas être en train d'accompagner le perso"), (4, "La cible doit être en train d'accompagner ce perso")], default=1, verbose_name='Cible Perso : accompagne un autre perso ?'),
        ),
    ]
