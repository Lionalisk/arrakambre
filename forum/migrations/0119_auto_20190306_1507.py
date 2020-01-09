# Generated by Django 2.1.1 on 2019-03-06 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0118_auto_20190306_1452'),
    ]

    operations = [
        migrations.AddField(
            model_name='posture',
            name='condition_cache',
            field=models.SmallIntegerField(choices=[(0, 'Peut etre fait si le perso est caché ou non'), (1, "Ne peut etre fait que si le perso n'est pas caché"), (2, 'Ne peut être fait que si le perso est caché')], default=0),
        ),
        migrations.AddField(
            model_name='posture',
            name='condition_espece',
            field=models.ManyToManyField(blank=True, related_name='espece_condition_posture', to='forum.Espece', verbose_name="Condition d'espèce pour adopter cette Posture"),
        ),
        migrations.AddField(
            model_name='posture',
            name='condition_hote',
            field=models.SmallIntegerField(choices=[(0, 'Peut etre fait si le perso est un hote de lieu ou non'), (1, "Ne peut etre fait que si le perso n'est pas un hote de lieu"), (2, 'Ne peut être fait que si le perso est un hote de lieu')], default=1),
        ),
    ]