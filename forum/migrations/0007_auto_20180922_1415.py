# Generated by Django 2.1.1 on 2018-09-22 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0006_auto_20180922_1413'),
    ]

    operations = [
        migrations.AlterField(
            model_name='maison',
            name='description',
            field=models.TextField(blank=True, default=''),
        ),
    ]