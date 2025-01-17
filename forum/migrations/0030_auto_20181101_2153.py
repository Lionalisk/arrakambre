# Generated by Django 2.1.1 on 2018-11-01 20:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0029_remove_action_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Espece',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=30, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='perso',
            name='situation',
        ),
        migrations.AddField(
            model_name='action',
            name='ciblelieu_acote',
            field=models.SmallIntegerField(choices=[(0, 'Le lieu cible peut être éloigné ou non'), (1, 'Le lieu présent doit avoir un passage vers le lieu cible'), (2, 'Le lieu présent ne doit pas avoir de passage vers le lieu cible')], default=1, verbose_name='Cible Lieu : éloignée ?'),
        ),
        migrations.AddField(
            model_name='action',
            name='cibleperso_PV_max',
            field=models.SmallIntegerField(default=10),
        ),
        migrations.AddField(
            model_name='action',
            name='cibleperso_PV_min',
            field=models.SmallIntegerField(default=1),
        ),
        migrations.AddField(
            model_name='action',
            name='cibleperso_eloigne',
            field=models.SmallIntegerField(choices=[(0, 'La cible peut être dans le même lieu ou non'), (1, 'La cible doit être dans le même lieu'), (2, 'La cible ne doit pas être dans le même lieu')], default=1, verbose_name='Cible Perso : éloignée ?'),
        ),
        migrations.AddField(
            model_name='action',
            name='cibleperso_encombat',
            field=models.SmallIntegerField(choices=[(0, 'La cible peut être en combat ou non'), (1, 'La cible ne doit pas être en combat'), (2, 'La cible doit être en combat')], default=0, verbose_name='Cible Perso : en combat ?'),
        ),
        migrations.AddField(
            model_name='action',
            name='cibleperso_est_accompagnant',
            field=models.SmallIntegerField(choices=[(0, 'La cible peut accompagner un autre perso ou non'), (1, "La cible ne doit pas être en train d'accompagner un autre perso"), (2, "La cible doit être en train d'accompagner un autre perso")], default=1, verbose_name='Cible Perso : accompagne un autre perso ?'),
        ),
        migrations.AddField(
            model_name='action',
            name='cibleperso_est_leader',
            field=models.SmallIntegerField(choices=[(0, 'La cible peut être en train de mener le perso ou non'), (1, 'La cible ne doit pas être en train de mener le perso'), (2, 'La cible doit être en train de mener le perso')], default=0, verbose_name='Cible Perso : est en train de mener le perso ?'),
        ),
        migrations.AddField(
            model_name='action',
            name='cibleperso_occupe',
            field=models.SmallIntegerField(choices=[(0, 'La cible peut être occupée ou non'), (1, "Ne peut etre fait que si la cible n'est pas occupée"), (2, 'Ne peut être fait que si la cible est occupée')], default=0, verbose_name='Cible Perso : occupée ?'),
        ),
        migrations.AddField(
            model_name='action',
            name='cibleperso_prisonnier',
            field=models.SmallIntegerField(choices=[(0, 'La cible peut être prisonnier ou non'), (1, 'La cible ne doit pas être prisonnier'), (2, 'La cible doit être prisonnier')], default=1, verbose_name='Cible Perso : prisonnier ?'),
        ),
        migrations.AddField(
            model_name='perso',
            name='espece',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='espece', to='forum.Espece'),
        ),
    ]
