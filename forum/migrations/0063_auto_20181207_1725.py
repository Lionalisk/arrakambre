# Generated by Django 2.1.3 on 2018-12-07 16:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0062_auto_20181207_1402'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perso',
            name='etat_sante',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='forum.Sante'),
        ),
    ]
