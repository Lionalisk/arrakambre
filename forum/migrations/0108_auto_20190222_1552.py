# Generated by Django 2.1.3 on 2019-02-22 14:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0107_auto_20190222_1529'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='loi',
            name='description',
        ),
        migrations.AddField(
            model_name='loi',
            name='post',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='forum.Post'),
        ),
    ]