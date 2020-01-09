# Generated by Django 2.1.3 on 2018-12-04 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0055_auto_20181130_1833'),
    ]

    operations = [
        migrations.CreateModel(
            name='Categorie_action',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=30, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('priorite', models.SmallIntegerField(default=1)),
            ],
        ),
    ]
