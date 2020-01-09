# Generated by Django 2.1.3 on 2019-11-12 10:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0220_auto_20191105_1725'),
    ]

    operations = [
        migrations.AddField(
            model_name='resultat',
            name='competence',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='resultat_copetence', to='forum.Competence', verbose_name="competence : si blank, prend la compétence associée à l'action"),
        ),
    ]