# Generated by Django 2.1.3 on 2019-09-30 16:45

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0195_auto_20190927_1115'),
    ]

    operations = [
        migrations.CreateModel(
            name='Effet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True)),
                ('nom', models.CharField(max_length=30, unique=True)),
                ('classe', models.CharField(default='', max_length=100)),
                ('val_competence_bonifie', models.SmallIntegerField(default=0)),
                ('val_posture_bonifie', models.SmallIntegerField(default=0)),
                ('bonus_combat', models.SmallIntegerField(default=0)),
                ('bonus_PV', models.SmallIntegerField(default=0)),
                ('bonus_PA', models.SmallIntegerField(default=0)),
                ('bonus_PC', models.SmallIntegerField(default=0)),
                ('bonus_PE', models.SmallIntegerField(default=0)),
                ('date_debut', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_fin', models.DateTimeField(default=django.utils.timezone.now)),
                ('fini', models.BooleanField(default=False)),
                ('commence', models.BooleanField(default=False)),
                ('erreur', models.BooleanField(default=False)),
                ('competence_bonifie', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='effet_comp_bonus', to='forum.Competence')),
                ('objet', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='effet_objet', to='forum.Objet_perso')),
            ],
        ),
        migrations.RemoveField(
            model_name='perso',
            name='PA_MAX',
        ),
        migrations.AddField(
            model_name='effet',
            name='perso',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='effet_perso', to='forum.Perso'),
        ),
        migrations.AddField(
            model_name='effet',
            name='posture_bonifie',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='effet_posture_bonus', to='forum.Posture'),
        ),
    ]
