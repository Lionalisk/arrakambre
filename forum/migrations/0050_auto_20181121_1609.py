# Generated by Django 2.1.3 on 2018-11-21 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0049_auto_20181118_2142'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='info_MJ',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='action',
            name='condition_lieuQG',
            field=models.SmallIntegerField(choices=[(0, 'Peut etre fait si le lieu dans lequel est le perso est un QG ou non'), (1, "Ne peut etre fait que si le lieu dans lequel est le perso n'est pas un QG"), (2, 'Ne peut etre fait que si le lieu dans lequel est le perso est un QG')], default=0),
        ),
        migrations.AlterField(
            model_name='action',
            name='condition_lieu_espace',
            field=models.SmallIntegerField(choices=[(0, 'Peut etre fait si le lieu dans lequel est le perso est un grand espace ou non'), (1, "Ne peut etre fait que si le lieu dans lequel est le perso n'est pas un grand espace"), (2, 'Ne peut etre fait que si le lieu dans lequel est le perso est un grand espace')], default=0),
        ),
        migrations.AlterField(
            model_name='action',
            name='condition_lieuferme',
            field=models.SmallIntegerField(choices=[(0, 'Peut etre fait si le lieu dans lequel est le perso est fermé ou non'), (1, "Ne peut etre fait que si le lieu dans lequel est le perso n'est pas fermé"), (2, 'Ne peut etre fait que si le lieu dans lequel est le perso est fermé')], default=0),
        ),
    ]
