# Generated by Django 2.1.3 on 2019-04-30 15:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0130_auto_20190430_1749'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='perso_etatsante',
            field=models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, to='forum.Sante'),
        ),
    ]
