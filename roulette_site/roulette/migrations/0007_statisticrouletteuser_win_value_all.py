# Generated by Django 4.0.4 on 2022-04-30 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roulette', '0006_round_user_alter_bet_user_statisticrouletteuser'),
    ]

    operations = [
        migrations.AddField(
            model_name='statisticrouletteuser',
            name='win_value_all',
            field=models.IntegerField(null=True, verbose_name='All wins value'),
        ),
    ]
