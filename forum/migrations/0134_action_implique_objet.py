# Generated by Django 2.1.3 on 2019-05-02 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0133_commande_objet_implique'),
    ]

    operations = [
        migrations.AddField(
            model_name='action',
            name='implique_objet',
            field=models.BooleanField(default=False, verbose_name='implique un objet'),
        ),
    ]