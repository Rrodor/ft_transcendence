# Generated by Django 4.2 on 2024-01-16 01:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0008_tournament_tournamentplayer'),
    ]

    operations = [
        migrations.AddField(
            model_name='tournament',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
