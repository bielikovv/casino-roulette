# Generated by Django 4.0.4 on 2022-04-28 14:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('roulette', '0003_alter_profile_balance'),
    ]

    operations = [
        migrations.CreateModel(
            name='Round',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color', models.CharField(max_length=30, verbose_name='Random color')),
            ],
        ),
        migrations.CreateModel(
            name='Bet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(auto_now_add=True, verbose_name='Time')),
                ('color', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='roulette.rouletteblock', verbose_name='Color')),
                ('round', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='roulette.round', verbose_name='Round')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
        ),
    ]
