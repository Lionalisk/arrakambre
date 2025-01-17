# Generated by Django 2.1.3 on 2019-10-01 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0197_auto_20191001_1632'),
    ]

    operations = [
        migrations.AddField(
            model_name='effet',
            name='priorite',
            field=models.SmallIntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='effet',
            name='classe',
            field=models.CharField(choices=[('potion', 'potion'), ('benediction', 'benediction'), ('malediction', 'malediction'), ('poison', 'poison'), ('charme', 'charme'), ('maladie', 'maladie'), ('', 'divers')], default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='effet',
            name='delai',
            field=models.SmallIntegerField(default=100),
        ),
    ]
