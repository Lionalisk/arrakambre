# Generated by Django 2.1.3 on 2019-12-04 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0234_auto_20191202_1427'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='text_persos_cible',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
    ]
