# Generated by Django 2.1.3 on 2019-10-14 13:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0209_auto_20191014_1516'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='perso_nom_info',
            new_name='perso_image',
        ),
    ]
