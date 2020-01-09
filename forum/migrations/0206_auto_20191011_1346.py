# Generated by Django 2.1.3 on 2019-10-11 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0205_auto_20191010_1437'),
    ]

    operations = [
        migrations.AlterField(
            model_name='effet',
            name='classe',
            field=models.CharField(blank=True, choices=[('potion', 'potion'), ('benediction', 'benediction'), ('malediction', 'malediction'), ('poison', 'poison'), ('charme', 'charme'), ('maladie', 'maladie'), ('', 'divers')], default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='objet',
            name='classe',
            field=models.CharField(blank=True, choices=[('arme', 'arme'), ('armure', 'armure'), ('potion', 'potion'), ('poison', 'poison'), ('parchemin', 'parchemin'), ('rituel', 'grimoire de rituel'), ('artefact', 'artefact'), ('quete', 'objet de quete'), ('', 'divers')], default='', max_length=100),
        ),
    ]