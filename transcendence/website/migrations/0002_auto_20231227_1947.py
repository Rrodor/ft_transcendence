# Generated by Django 3.2.18 on 2023-12-27 19:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='pong_defeats',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='pong_victories',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='total_pong_games',
            field=models.IntegerField(default=0),
        ),
    ]
