# Generated by Django 2.1.3 on 2019-09-20 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0188_objet_classe'),
    ]

    operations = [
        migrations.AlterField(
            model_name='objet',
            name='special',
            field=models.CharField(blank=True, default='', max_length=30, null=True),
        ),
    ]