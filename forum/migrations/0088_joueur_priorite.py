# Generated by Django 2.1.3 on 2019-01-29 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0087_auto_20190124_1440'),
    ]

    operations = [
        migrations.AddField(
            model_name='joueur',
            name='priorite',
            field=models.SmallIntegerField(default=1),
        ),
    ]