# Generated by Django 2.1.3 on 2019-07-15 12:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0167_auto_20190715_1156'),
    ]

    operations = [
        migrations.AddField(
            model_name='langage',
            name='competence',
            field=models.ForeignKey(default=8, on_delete=django.db.models.deletion.SET_DEFAULT, related_query_name='competence_langage', to='forum.Competence'),
        ),
        migrations.AddField(
            model_name='langage',
            name='niveau',
            field=models.SmallIntegerField(default=2),
        ),
        migrations.AlterField(
            model_name='langage',
            name='alphabet_langue',
            field=models.TextField(default='a-;-b-;-c-;-d-;-e-;-f-;-g-;-h-;-i-;-j-;-k-;-l-;-m-;-n-;-o-;-p-;-q-;-r-;-s-;-t-;-u-;-v-;-w-;-x-;-y-;-z-;-0-;-1-;-2-;-3-;-4-;-5-;-6-;-7-;-8-;-9-;-é-;-à-;-è-;-,-;-.-;-;', verbose_name='Alphabet Correspondant(-;- entre chaque caractère)'),
        ),
    ]