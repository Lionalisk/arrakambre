# Generated by Django 2.1.3 on 2019-01-24 13:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0085_auto_20190124_1221'),
    ]

    operations = [
        migrations.AddField(
            model_name='perso',
            name='classe_principale',
            field=models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='classe_principale', to='forum.Categorie_competence'),
        ),
        migrations.AddField(
            model_name='perso',
            name='classe_secondaire',
            field=models.ForeignKey(default=2, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='classe_secondaire', to='forum.Categorie_competence'),
        ),
    ]
