# Generated by Django 2.1.3 on 2019-09-17 17:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0186_auto_20190917_1649'),
    ]

    operations = [
        migrations.RenameField(
            model_name='maison',
            old_name='Suzerain',
            new_name='suzerain',
        ),
    ]
