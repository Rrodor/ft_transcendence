# Generated by Django 4.2 on 2024-01-16 02:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0014_tournament_players'),
    ]

    operations = [
        migrations.AddField(
            model_name='tournament',
            name='is_started',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score_participant1', models.IntegerField(blank=True, null=True)),
                ('score_participant2', models.IntegerField(blank=True, null=True)),
                ('participant1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='matches_as_player1', to='website.participant')),
                ('participant2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='matches_as_player2', to='website.participant')),
                ('tournament', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='matches', to='website.tournament')),
                ('winner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='won_matches', to='website.participant')),
            ],
        ),
    ]
