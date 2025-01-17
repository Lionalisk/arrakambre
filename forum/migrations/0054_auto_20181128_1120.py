# Generated by Django 2.1.3 on 2018-11-28 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0053_auto_20181126_1426'),
    ]

    operations = [
        migrations.AddField(
            model_name='competence',
            name='nom_info',
            field=models.CharField(max_length=40, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='perso',
            name='PE',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='perso',
            name='PE_MAX',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
