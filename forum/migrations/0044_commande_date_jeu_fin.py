# Generated by Django 2.1.1 on 2018-11-10 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0043_auto_20181110_1110'),
    ]

    operations = [
        migrations.AddField(
            model_name='commande',
            name='date_jeu_fin',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
    ]
