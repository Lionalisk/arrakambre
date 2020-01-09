# Generated by Django 2.1.3 on 2019-02-06 16:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0091_post_nom_info'),
    ]

    operations = [
        migrations.CreateModel(
            name='Resultat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True)),
                ('type', models.SmallIntegerField(choices=[(0, 'Autre'), (1, 'Fouille'), (2, 'Bibliotheque'), (3, 'Enquete'), (3, 'Exploration')], default=0)),
                ('nom', models.CharField(max_length=30, unique=True, verbose_name='Titre du resultat')),
                ('description', models.TextField(blank=True, default='', null=True, verbose_name='Description MJ')),
                ('cle1', models.CharField(max_length=30, unique=True, verbose_name="Clé 1 - ';' sépare les entités ")),
                ('cle2', models.CharField(max_length=300, unique=True, verbose_name="Clé 2 - ';' sépare les entités ")),
                ('cle_date', models.CharField(max_length=100, unique=True, verbose_name='Clé Date')),
                ('dommage', models.SmallIntegerField(default=9)),
                ('unique', models.BooleanField(default=False)),
                ('fini', models.BooleanField(default=False)),
                ('Lieu', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='lieu_recherche', to='forum.Lieu')),
                ('attaquer_par', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='attaquer_par', to='forum.Perso')),
                ('commande_suivante', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='commande_suivante', to='forum.Commande')),
                ('objet_trouve', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='objet_trouve', to='forum.Objet')),
                ('passage_trouve', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='passage_trouve', to='forum.Lieu')),
                ('perso_trouve', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='perso_trouve', to='forum.Perso')),
                ('post', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='post_resultat', to='forum.Post')),
            ],
        ),
    ]
