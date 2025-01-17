# Generated by Django 2.1.1 on 2018-11-07 20:57

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0040_jeu'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mois',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=30, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('numero', models.SmallIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)], verbose_name="numero du mois dans l'année")),
            ],
        ),
        migrations.RenameField(
            model_name='commande',
            old_name='date_validation',
            new_name='date_fin',
        ),
        migrations.RemoveField(
            model_name='commande',
            name='en_attente',
        ),
        migrations.AddField(
            model_name='action',
            name='cibleperso_espece',
            field=models.ManyToManyField(blank=True, related_name='espece_cibleperso', to='forum.Espece'),
        ),
        migrations.AddField(
            model_name='action',
            name='cibleperso_soimeme',
            field=models.BooleanField(default=False, verbose_name='Cible Perso : peut être soi-même ?'),
        ),
        migrations.AddField(
            model_name='action',
            name='condition_espece',
            field=models.ManyToManyField(blank=True, related_name='espece_condition', to='forum.Espece'),
        ),
        migrations.AddField(
            model_name='action',
            name='est_deplacement',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='action',
            name='post_only',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='action',
            name='programmable',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='commande',
            name='chance_reussite',
            field=models.SmallIntegerField(default=100),
        ),
        migrations.AddField(
            model_name='commande',
            name='commence',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='commande',
            name='date_debut',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='commande',
            name='erreur',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='commande',
            name='fini',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='commande',
            name='texte_post',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AddField(
            model_name='jeu',
            name='annee_jeu_init',
            field=models.SmallIntegerField(default=99),
        ),
        migrations.AddField(
            model_name='jeu',
            name='date_initiale',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='jeu',
            name='delay_suppr',
            field=models.DecimalField(decimal_places=2, default=4, max_digits=4, verbose_name='Temps avant de supprimer une action finie, en jours'),
        ),
        migrations.AddField(
            model_name='jeu',
            name='heure_jeu_init',
            field=models.SmallIntegerField(default=1, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(23)]),
        ),
        migrations.AddField(
            model_name='jeu',
            name='jour_jeu_init',
            field=models.SmallIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AddField(
            model_name='jeu',
            name='jour_par_mois',
            field=models.SmallIntegerField(default=31, validators=[django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AddField(
            model_name='jeu',
            name='mois_par_an',
            field=models.SmallIntegerField(default=12, validators=[django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AddField(
            model_name='jeu',
            name='rapport_temps',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=4, verbose_name="Combien d'heures réelles pour une heure de jeu ?"),
        ),
        migrations.AlterField(
            model_name='jeu',
            name='base_delay',
            field=models.DecimalField(decimal_places=4, default=1, max_digits=6, verbose_name='Délai pour une action courante, en heures'),
        ),
        migrations.AlterField(
            model_name='perso',
            name='genre',
            field=models.BooleanField(default=True, verbose_name='Le personnage est un homme ?'),
        ),
        migrations.AddField(
            model_name='jeu',
            name='mois_jeu_init',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to='forum.Mois'),
        ),
    ]
