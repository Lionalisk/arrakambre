# Generated by Django 2.1.3 on 2019-06-07 15:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0137_auto_20190606_1751'),
    ]

    operations = [
        migrations.AddField(
            model_name='perso',
            name='last_commande',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='last_commande_perso', to='forum.Commande'),
        ),
        migrations.AlterField(
            model_name='commande',
            name='instant_mois',
            field=models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, to='forum.Mois'),
        ),
    ]
