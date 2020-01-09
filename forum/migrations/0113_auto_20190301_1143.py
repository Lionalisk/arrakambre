# Generated by Django 2.1.3 on 2019-03-01 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0112_action_mj_only'),
    ]

    operations = [
        migrations.AlterField(
            model_name='action',
            name='ciblelieu_inconnu',
            field=models.SmallIntegerField(choices=[(0, 'Le lieu cible peut être un lieu inconnu ou non'), (1, 'Le lieu cible ne doit pas être un lieu inconnu pour le joueur'), (2, 'Le lieu cible doit être un lieu inconnu pour le joueur')], default=1, verbose_name='Cible Lieu : est inconnu ?'),
        ),
        migrations.AlterField(
            model_name='action',
            name='ciblelieu_secret',
            field=models.SmallIntegerField(choices=[(0, 'Le lieu cible peut être un lieu secret ou non'), (1, 'Le lieu cible ne doit pas être un lieu secret pour le joueur'), (2, 'Le lieu cible doit être un lieu secret pour le joueur')], default=0, verbose_name='Cible Lieu : est secret ?'),
        ),
    ]
