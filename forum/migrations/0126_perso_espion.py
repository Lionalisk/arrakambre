# Generated by Django 2.1.3 on 2019-04-30 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0125_auto_20190429_1154'),
    ]

    operations = [
        migrations.AddField(
            model_name='perso',
            name='espion',
            field=models.BooleanField(default=False),
        ),
    ]
