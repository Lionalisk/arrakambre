# Generated by Django 2.1.3 on 2018-12-07 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0061_action_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='action',
            name='condition_suit_perso',
            field=models.SmallIntegerField(choices=[(0, "Peut etre fait si le perso suit quelqu'un ou non"), (1, "Ne peut etre fait que si le perso n'est pas en train de suivre quelqu'un"), (2, "Ne peut être fait que si le perso est en train de suivre quelqu'un")], default=1),
        ),
        migrations.AlterField(
            model_name='action',
            name='options',
            field=models.BooleanField(default=False, verbose_name='a des options - Si oui, les actions lui rapportant doivent lui référer dans Action Parent. Les verifications de base se feront à partir de cette entité.'),
        ),
    ]
