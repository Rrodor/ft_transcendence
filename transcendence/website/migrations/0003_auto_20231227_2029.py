# Generated by Django 3.2.18 on 2023-12-27 20:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_auto_20231227_1947'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='pong_defeats_percentage',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='pong_victories_percentage',
            field=models.FloatField(default=0),
        ),
    ]
