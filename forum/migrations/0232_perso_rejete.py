# Generated by Django 2.1.3 on 2019-11-21 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0231_perso_comportement_intervention'),
    ]

    operations = [
        migrations.AddField(
            model_name='perso',
            name='rejete',
            field=models.BooleanField(default=False, verbose_name='rejete : Est il rejeté de sa maison ?'),
        ),
    ]
