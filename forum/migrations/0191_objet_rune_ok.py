# Generated by Django 2.1.3 on 2019-09-20 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0190_auto_20190920_1007'),
    ]

    operations = [
        migrations.AddField(
            model_name='objet',
            name='rune_OK',
            field=models.BooleanField(default=False, verbose_name="rune_Ok : une rune est possible sur l'objet ?"),
        ),
    ]
