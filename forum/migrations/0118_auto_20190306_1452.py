# Generated by Django 2.1.1 on 2019-03-06 13:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0117_auto_20190306_1449'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perso',
            name='posture_defaut_duel',
            field=models.ForeignKey(default=8, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='posture_def_duel', to='forum.Posture'),
        ),
        migrations.AlterField(
            model_name='perso',
            name='posture_defaut_melee',
            field=models.ForeignKey(default=6, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='posture_def_melee', to='forum.Posture'),
        ),
    ]