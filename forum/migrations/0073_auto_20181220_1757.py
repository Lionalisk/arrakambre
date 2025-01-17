# Generated by Django 2.1.3 on 2018-12-20 16:57

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0072_maison_senateur'),
    ]

    operations = [
        migrations.CreateModel(
            name='Loi',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField(blank=True, default='', null=True)),
                ('votes', models.SmallIntegerField(default=0)),
                ('valide', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=True)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_validation', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_fin', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_jeu_fin', models.CharField(blank=True, default='', max_length=50)),
                ('date_jeu_validation', models.CharField(blank=True, default='', max_length=50)),
                ('commande', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='forum.Commande')),
                ('joueur', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='forum.Joueur')),
            ],
        ),
        migrations.AddField(
            model_name='maison',
            name='nb_voix_senat',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='loi',
            name='maison',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='forum.Maison'),
        ),
        migrations.AddField(
            model_name='loi',
            name='maison_a_vote',
            field=models.ManyToManyField(blank=True, related_name='maison_vote', to='forum.Maison'),
        ),
        migrations.AddField(
            model_name='loi',
            name='perso',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='forum.Perso'),
        ),
    ]
