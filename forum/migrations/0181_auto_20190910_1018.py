# Generated by Django 2.1.3 on 2019-09-10 08:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0180_auto_20190819_1451'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lieu',
            name='maison',
        ),
        migrations.AlterField(
            model_name='perso',
            name='joueur',
            field=models.ManyToManyField(blank=True, related_name='persos', to='forum.Joueur'),
        ),
    ]