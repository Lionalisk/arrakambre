# Generated by Django 2.1.3 on 2019-02-08 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0095_auto_20190207_1006'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lieu',
            name='atelier',
        ),
        migrations.AddField(
            model_name='lieu',
            name='atelier',
            field=models.ManyToManyField(related_name='atelier_lieu', to='forum.Atelier'),
        ),
    ]
