# Generated by Django 2.1.1 on 2018-09-26 19:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('forum', '0010_auto_20180922_1455'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lieu',
            name='persos_connaissants',
        ),
        migrations.AddField(
            model_name='lieu',
            name='priorite',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='lieu',
            name='priorite_temp',
            field=models.PositiveIntegerField(default=0, editable=False),
        ),
        migrations.AddField(
            model_name='lieu',
            name='users_connaissants',
            field=models.ManyToManyField(blank=True, related_name='users_connaissants', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='perso',
            name='priorite',
            field=models.SmallIntegerField(default=1),
        ),
        migrations.AddField(
            model_name='perso',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='post',
            name='persos_cible',
            field=models.ManyToManyField(blank=True, related_name='users_cible', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='post',
            name='published_date',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True),
        ),
    ]