# Generated by Django 2.1.3 on 2019-01-24 13:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0086_auto_20190124_1403'),
    ]

    operations = [
        migrations.AddField(
            model_name='competence',
            name='categorie_classement',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='categorie_classement', to='forum.Categorie_competence'),
        ),
        migrations.AlterField(
            model_name='competence',
            name='categorie',
            field=models.ManyToManyField(blank=True, related_name='categorie', to='forum.Categorie_competence'),
        ),
    ]
