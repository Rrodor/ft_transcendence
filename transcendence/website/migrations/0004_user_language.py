# Generated by Django 5.0.1 on 2024-01-12 00:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0003_user_pong_average_against_user_pong_average_for'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='language',
            field=models.CharField(default='en', max_length=2),
        ),
    ]