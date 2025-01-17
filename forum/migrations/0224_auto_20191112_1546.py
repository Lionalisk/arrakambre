# Generated by Django 2.1.3 on 2019-11-12 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0223_auto_20191112_1540'),
    ]

    operations = [
        migrations.AddField(
            model_name='resultat',
            name='users_possible',
            field=models.ManyToManyField(blank=True, related_name='peut_avoir_resultat', to='forum.Joueur'),
        ),
        migrations.AlterField(
            model_name='resultat',
            name='users_connaissants',
            field=models.ManyToManyField(blank=True, related_name='connaissants_resultat', to='forum.Joueur'),
        ),
    ]
