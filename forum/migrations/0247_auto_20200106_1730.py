# Generated by Django 2.1.3 on 2020-01-06 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0246_auto_20200106_1342'),
    ]

    operations = [
        migrations.AddField(
            model_name='lieu',
            name='gain_administration',
            field=models.SmallIntegerField(default=1),
        ),
        migrations.AddField(
            model_name='lieu',
            name='nom_action_administration',
            field=models.CharField(default='Administrer', max_length=100),
        ),
    ]
