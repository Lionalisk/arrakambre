# Generated by Django 2.1.1 on 2018-10-03 19:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0017_auto_20180930_1348'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sante',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=30, unique=True)),
                ('PV', models.SmallIntegerField(default=0)),
                ('image', models.CharField(max_length=30)),
            ],
        ),
        migrations.AddField(
            model_name='perso',
            name='comp_niv1',
            field=models.ManyToManyField(blank=True, related_name='comp_niv1', to='forum.Competence'),
        ),
        migrations.AddField(
            model_name='perso',
            name='comp_niv2',
            field=models.ManyToManyField(blank=True, related_name='comp_niv2', to='forum.Competence'),
        ),
        migrations.AddField(
            model_name='perso',
            name='comp_niv3',
            field=models.ManyToManyField(blank=True, related_name='comp_niv3', to='forum.Competence'),
        ),
        migrations.AddField(
            model_name='perso',
            name='comp_niv4',
            field=models.ManyToManyField(blank=True, related_name='comp_niv4', to='forum.Competence'),
        ),
        migrations.AlterField(
            model_name='perso',
            name='etat_sante',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='forum.Sante'),
        ),
        migrations.AlterField(
            model_name='perso',
            name='situation',
            field=models.CharField(blank=True, choices=[('', 'RAS'), ('Accompagnant', 'Accompagnant'), ('Prisonnier(e)', 'Prisonnier(e)'), ('En situation de combat', 'En situation de combat')], default='', max_length=30),
        ),
        migrations.AlterField(
            model_name='post',
            name='lieu',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_query_name='lieu_post', to='forum.Lieu'),
        ),
    ]