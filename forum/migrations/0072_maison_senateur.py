# Generated by Django 2.1.3 on 2018-12-19 15:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0071_auto_20181219_1605'),
    ]

    operations = [
        migrations.AddField(
            model_name='maison',
            name='senateur',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='senateur', to='forum.Perso'),
        ),
    ]