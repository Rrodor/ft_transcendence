# Generated by Django 4.2 on 2024-01-16 01:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0011_tournament_nb_players'),
    ]

    operations = [
        migrations.DeleteModel(
            name='TournamentPlayer',
        ),
    ]