# Generated by Django 2.1.3 on 2019-10-14 13:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0208_auto_20191011_1819'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='perso',
            name='ID_nom_info',
        ),
        migrations.AddField(
            model_name='post',
            name='perso_capture',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='post',
            name='perso_maison',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='forum.Maison'),
        ),
        migrations.AddField(
            model_name='post',
            name='perso_nom',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='perso_nom_info',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='perso_titre',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
