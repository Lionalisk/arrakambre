# Generated by Django 2.1.3 on 2019-11-15 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0225_auto_20191114_1715'),
    ]

    operations = [
        migrations.AddField(
            model_name='perso',
            name='defense',
            field=models.SmallIntegerField(default=4),
        ),
        migrations.AddField(
            model_name='perso',
            name='protection',
            field=models.SmallIntegerField(default=2),
        ),
        migrations.AlterField(
            model_name='regle',
            name='nom',
            field=models.CharField(max_length=60),
        ),
    ]