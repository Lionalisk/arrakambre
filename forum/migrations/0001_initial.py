# Generated by Django 2.1.1 on 2018-09-08 20:23

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Lieu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=30)),
                ('desc', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Maison',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=30)),
                ('desc', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Perso',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=30)),
                ('desc', models.TextField()),
                ('lieu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='forum.Lieu')),
                ('maison', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='forum.Maison')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titre', models.CharField(max_length=200)),
                ('texte', models.TextField()),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('published_date', models.DateTimeField(blank=True, null=True)),
                ('lieu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='forum.Lieu')),
                ('perso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='forum.Perso')),
            ],
        ),
        migrations.AddField(
            model_name='lieu',
            name='maison',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='forum.Maison'),
        ),
    ]