# Generated by Django 2.1.1 on 2018-11-18 20:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0048_auto_20181117_1022'),
    ]

    operations = [
        migrations.AddField(
            model_name='action',
            name='condition_lieuQG',
            field=models.SmallIntegerField(choices=[(0, 'Peut etre fait si le lieu dans lequel est le perso est un grand espace ou non'), (1, "Ne peut etre fait que si le lieu dans lequel est le perso n'est pas un grand espace"), (2, 'Ne peut etre fait que si le lieu dans lequel est le perso est lun grand espace')], default=0),
        ),
        migrations.AddField(
            model_name='action',
            name='condition_lieu_agardes',
            field=models.SmallIntegerField(choices=[(0, 'Peut etre fait si le lieu dans lequel est le perso a des gardes ou non'), (1, "Ne peut etre fait que si le lieu dans lequel est le perso n'a pas de gardes"), (2, 'Ne peut etre fait que si le lieu dans lequel est le perso a des gardes')], default=0),
        ),
        migrations.AddField(
            model_name='action',
            name='condition_lieu_atroupes',
            field=models.SmallIntegerField(choices=[(0, 'Peut etre fait si le lieu dans lequel est le perso a des troupes ou non'), (1, "Ne peut etre fait que si le lieu dans lequel est le perso n'a pas de troupes"), (2, 'Ne peut etre fait que si le lieu dans lequel est le perso a des troupes')], default=0),
        ),
        migrations.AddField(
            model_name='action',
            name='condition_lieu_espace',
            field=models.SmallIntegerField(choices=[(0, 'Peut etre fait si le lieu dans lequel est le perso est un QG ou non'), (1, "Ne peut etre fait que si le lieu dans lequel est le perso n'est pas un QG"), (2, 'Ne peut etre fait que si le lieu dans lequel est le perso est un QG')], default=0),
        ),
        migrations.AddField(
            model_name='action',
            name='condition_lieu_propriete',
            field=models.SmallIntegerField(choices=[(0, 'Peut etre fait si le lieu dans lequel est le perso est la propriété de sa maison ou non'), (1, "Ne peut etre fait que si le lieu dans lequel est le perso n'est pas la propriété de sa maison"), (2, 'Ne peut etre fait que si le lieu dans lequel est le perso est la propriété de sa maison')], default=0),
        ),
        migrations.AddField(
            model_name='action',
            name='condition_lieuferme',
            field=models.SmallIntegerField(choices=[(0, 'Peut etre fait si le lieu dans lequel est le perso est fermé ou non'), (1, "Ne peut etre fait que si le lieu dans lequel est le perso n'est pas fermé"), (2, 'Ne peut etre fait que si le lieu dans lequel est le perso est pas fermé')], default=0),
        ),
        migrations.AlterField(
            model_name='action',
            name='msg_encours',
            field=models.CharField(blank=True, default='', max_length=200, null=True, verbose_name="Phrase d'information lorsque la commande est encours(#perso# , #lieu# , #persos_cible# , #lieux_cible#)"),
        ),
    ]