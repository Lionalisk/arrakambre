# Generated by Django 2.1.1 on 2018-10-06 20:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0023_auto_20181006_1414'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perso',
            name='etat_sante',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to='forum.Sante'),
        ),
    ]
