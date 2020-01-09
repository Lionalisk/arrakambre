# Generated by Django 2.1.3 on 2019-12-05 13:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0235_post_text_persos_cible'),
    ]

    operations = [
        migrations.AddField(
            model_name='perso',
            name='espionne',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='espions', to='forum.Perso', verbose_name="Qui le perso est en train d'espionner"),
        ),
    ]