# Generated by Django 2.1.3 on 2019-12-05 15:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0236_perso_espionne'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='resultat',
            name='objet_trouve',
        ),
        migrations.AddField(
            model_name='resultat',
            name='add_resultat',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='resultat_additionnel', to='forum.Resultat'),
        ),
        migrations.AddField(
            model_name='resultat',
            name='effet_recu',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='effet_trouve', to='forum.Effet'),
        ),
        migrations.AddField(
            model_name='resultat',
            name='modif_gardes',
            field=models.SmallIntegerField(blank=True, default=0),
        ),
        migrations.AddField(
            model_name='resultat',
            name='modif_troupes',
            field=models.SmallIntegerField(blank=True, default=0),
        ),
        migrations.RemoveField(
            model_name='resultat',
            name='resultat_trouve',
        ),
        migrations.AddField(
            model_name='resultat',
            name='resultat_trouve',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='resultat_pour_le_trouver', to='forum.Resultat'),
        ),
    ]
