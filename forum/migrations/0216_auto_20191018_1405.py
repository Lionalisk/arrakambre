# Generated by Django 2.1.3 on 2019-10-18 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0215_auto_20191017_1540'),
    ]

    operations = [
        migrations.AlterField(
            model_name='objet',
            name='nom',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
