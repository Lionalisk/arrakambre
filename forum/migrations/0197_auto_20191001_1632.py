# Generated by Django 2.1.3 on 2019-10-01 14:32

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0196_auto_20190930_1845'),
    ]

    operations = [
        migrations.CreateModel(
            name='Effet_perso',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_debut', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_fin', models.DateTimeField(default=django.utils.timezone.now)),
                ('fini', models.BooleanField(default=False)),
                ('commence', models.BooleanField(default=False)),
                ('erreur', models.BooleanField(default=False)),
            ],
        ),
        migrations.RemoveField(
            model_name='effet',
            name='commence',
        ),
        migrations.RemoveField(
            model_name='effet',
            name='date_debut',
        ),
        migrations.RemoveField(
            model_name='effet',
            name='date_fin',
        ),
        migrations.RemoveField(
            model_name='effet',
            name='erreur',
        ),
        migrations.RemoveField(
            model_name='effet',
            name='fini',
        ),
        migrations.RemoveField(
            model_name='effet',
            name='objet',
        ),
        migrations.RemoveField(
            model_name='effet',
            name='perso',
        ),
        migrations.RemoveField(
            model_name='objet',
            name='bonus_PA',
        ),
        migrations.RemoveField(
            model_name='objet',
            name='bonus_PC',
        ),
        migrations.RemoveField(
            model_name='objet',
            name='bonus_PE',
        ),
        migrations.RemoveField(
            model_name='objet',
            name='bonus_PV',
        ),
        migrations.RemoveField(
            model_name='objet',
            name='bonus_combat',
        ),
        migrations.RemoveField(
            model_name='objet',
            name='competence_bonifie',
        ),
        migrations.RemoveField(
            model_name='objet',
            name='posture_bonifie',
        ),
        migrations.AddField(
            model_name='effet',
            name='delai',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='effet',
            name='effet_suivant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='effet_parent', to='forum.Effet'),
        ),
        migrations.AddField(
            model_name='effet',
            name='negatif',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='effet',
            name='support',
            field=models.CharField(choices=[('perso', 'perso'), ('arme', 'arme'), ('armure', 'armure'), ('', 'divers')], default='', max_length=100),
        ),
        migrations.AddField(
            model_name='objet',
            name='effet',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='obj_effet', to='forum.Effet', verbose_name="effet : si Null et action Null, on ne peut pas utiliser l'objet"),
        ),
        migrations.AlterField(
            model_name='objet',
            name='action',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='obj_declenche', to='forum.Action', verbose_name='action : '),
        ),
        migrations.AlterField(
            model_name='objet',
            name='delay',
            field=models.SmallIntegerField(default=0, verbose_name="Pour arme = valeur d'initiative en %"),
        ),
        migrations.AddField(
            model_name='effet_perso',
            name='eft',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='perso_effet', to='forum.Effet'),
        ),
        migrations.AddField(
            model_name='effet_perso',
            name='objet',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='effet_objet', to='forum.Objet'),
        ),
        migrations.AddField(
            model_name='effet_perso',
            name='perso',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='effet_perso', to='forum.Perso'),
        ),
    ]
