# Generated by Django 2.1.1 on 2018-09-22 12:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0005_objet'),
    ]

    operations = [
        migrations.CreateModel(
            name='Action',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=40, unique=True)),
                ('nom_info', models.CharField(max_length=30, unique=True)),
                ('image', models.CharField(max_length=30, unique=True)),
                ('description', models.TextField(blank=True, default='', null=True)),
                ('priorite', models.SmallIntegerField(default=1)),
                ('PA', models.SmallIntegerField(default=1)),
                ('delay', models.SmallIntegerField(default=1)),
                ('is_objet', models.BooleanField(default=False)),
                ('is_lieu', models.BooleanField(default=False)),
                ('empechable', models.BooleanField(default=True)),
                ('dissimulable', models.BooleanField(default=True)),
                ('interdit', models.BooleanField(default=False)),
                ('cible_perso', models.BooleanField(default=False)),
                ('cible_persos', models.BooleanField(default=False)),
                ('cible_lieu', models.BooleanField(default=False)),
                ('cible_lieux', models.BooleanField(default=False)),
                ('cible_heure', models.BooleanField(default=False)),
                ('cible_action', models.BooleanField(default=False)),
                ('champ_recherche1', models.BooleanField(default=False)),
                ('champ_recherche2', models.BooleanField(default=False)),
                ('champ_texte', models.BooleanField(default=False)),
                ('msg', models.TextField(blank=True, default='', null=True)),
                ('msg_resume', models.TextField(blank=True, default='', null=True)),
                ('signal_MJ', models.SmallIntegerField(default=0)),
                ('msg_MJ', models.TextField(blank=True, default='', null=True)),
                ('action_parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='forum.Action')),
            ],
        ),
        migrations.CreateModel(
            name='Competence',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=40, unique=True)),
                ('description', models.TextField(blank=True, default='', null=True)),
                ('priorite', models.SmallIntegerField(default=0)),
            ],
        ),
        migrations.RemoveField(
            model_name='lieu',
            name='desc',
        ),
        migrations.RemoveField(
            model_name='perso',
            name='desc',
        ),
        migrations.AddField(
            model_name='lieu',
            name='defense_assault',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='lieu',
            name='defense_garde',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='lieu',
            name='defense_intrusion',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='lieu',
            name='description',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='lieu',
            name='dissimulation',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='lieu',
            name='image',
            field=models.CharField(default='lieu_none.jpg', max_length=40),
        ),
        migrations.AddField(
            model_name='lieu',
            name='lieu_parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='forum.Lieu', verbose_name='Lieu'),
        ),
        migrations.AddField(
            model_name='lieu',
            name='passages',
            field=models.ManyToManyField(blank=True, related_name='_lieu_passages_+', to='forum.Lieu'),
        ),
        migrations.AddField(
            model_name='lieu',
            name='perso_autorise',
            field=models.ManyToManyField(blank=True, related_name='persos_autorises', to='forum.Perso'),
        ),
        migrations.AddField(
            model_name='lieu',
            name='persos_connaissants',
            field=models.ManyToManyField(blank=True, related_name='persos_connaissants', to='forum.Perso'),
        ),
        migrations.AddField(
            model_name='lieu',
            name='proprietaire',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='proprietaire', to='forum.Perso'),
        ),
        migrations.AddField(
            model_name='lieu',
            name='secret',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='perso',
            name='Objets',
            field=models.ManyToManyField(related_name='objets', to='forum.Objet'),
        ),
        migrations.AddField(
            model_name='perso',
            name='PA',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='perso',
            name='PA_MAX',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='perso',
            name='PV',
            field=models.SmallIntegerField(default=3),
        ),
        migrations.AddField(
            model_name='perso',
            name='PVA',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='perso',
            name='PVA_MAX',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='perso',
            name='PV_MAX',
            field=models.PositiveIntegerField(default=3),
        ),
        migrations.AddField(
            model_name='perso',
            name='accompagnants',
            field=models.ManyToManyField(blank=True, related_name='_perso_accompagnants_+', to='forum.Perso'),
        ),
        migrations.AddField(
            model_name='perso',
            name='arme',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='arme', to='forum.Objet'),
        ),
        migrations.AddField(
            model_name='perso',
            name='armure',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='armure', to='forum.Objet'),
        ),
        migrations.AddField(
            model_name='perso',
            name='attaque_duel',
            field=models.SmallIntegerField(default=0, editable=False),
        ),
        migrations.AddField(
            model_name='perso',
            name='attaque_melee',
            field=models.SmallIntegerField(default=0, editable=False),
        ),
        migrations.AddField(
            model_name='perso',
            name='defense_duel',
            field=models.SmallIntegerField(default=0, editable=False),
        ),
        migrations.AddField(
            model_name='perso',
            name='defense_melee',
            field=models.SmallIntegerField(default=0, editable=False),
        ),
        migrations.AddField(
            model_name='perso',
            name='description',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AddField(
            model_name='perso',
            name='dissimulation',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='perso',
            name='en_main',
            field=models.ManyToManyField(related_name='en_main', to='forum.Objet'),
        ),
        migrations.AddField(
            model_name='perso',
            name='etat_sante',
            field=models.CharField(choices=[('MORT', 'Mort'), ('INC', 'Inconscient'), ('BLESSE2', 'Gravement Blesse'), ('BLESSE1', 'Blesse'), ('OK', 'En bonne sante')], default='OK', max_length=30),
        ),
        migrations.AddField(
            model_name='perso',
            name='genre',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='perso',
            name='initiative',
            field=models.SmallIntegerField(default=0, editable=False),
        ),
        migrations.AddField(
            model_name='perso',
            name='nbGardes',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='perso',
            name='nbTroupes',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='perso',
            name='prisonnier',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='forum.Perso'),
        ),
        migrations.AddField(
            model_name='perso',
            name='situation',
            field=models.CharField(choices=[('RAS', 'RAS'), ('ACCOMPAGNE', 'Accompagnant'), ('PRISONNIER', 'Prisonnier(e)'), ('COMBAT', 'En situation de combat')], default='RAS', max_length=30),
        ),
        migrations.AddField(
            model_name='perso',
            name='titre',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
        migrations.AddField(
            model_name='perso',
            name='volume_MAX',
            field=models.SmallIntegerField(default=5),
        ),
        migrations.AddField(
            model_name='post',
            name='dissimulation',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='post',
            name='valide',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='lieu',
            name='maison',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='forum.Maison', verbose_name='Maison'),
        ),
        migrations.AlterField(
            model_name='lieu',
            name='nom',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='objet',
            name='description',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='objet',
            name='pouvoir',
            field=models.CharField(blank=True, default='', max_length=30),
        ),
        migrations.AlterField(
            model_name='perso',
            name='image',
            field=models.CharField(default='perso_none.jpg', max_length=40),
        ),
        migrations.AlterField(
            model_name='perso',
            name='lieu',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='localisation', to='forum.Lieu'),
        ),
        migrations.AlterField(
            model_name='perso',
            name='maison',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='forum.Maison'),
        ),
        migrations.AlterField(
            model_name='perso',
            name='nom',
            field=models.CharField(max_length=30, unique=True),
        ),
        migrations.AddField(
            model_name='action',
            name='competences_utiles',
            field=models.ManyToManyField(to='forum.Competence'),
        ),
        migrations.AddField(
            model_name='action',
            name='condition_lieu',
            field=models.ManyToManyField(to='forum.Lieu'),
        ),
        migrations.AddField(
            model_name='post',
            name='action',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='forum.Action'),
        ),
    ]
