# Generated by Django 2.1.3 on 2019-11-15 17:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0227_auto_20191115_1826'),
    ]

    operations = [
        migrations.RenameField(
            model_name='effet',
            old_name='bonus_endurance',
            new_name='bonus_protection',
        ),
    ]
