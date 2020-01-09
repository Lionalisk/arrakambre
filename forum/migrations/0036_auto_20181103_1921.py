# Generated by Django 2.1.1 on 2018-11-03 18:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0035_auto_20181103_1914'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='etape_action',
            field=models.CharField(blank=True, default='', max_length=30),
        ),
        migrations.AddField(
            model_name='post',
            name='joueur',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='forum.Joueur'),
        ),
    ]
