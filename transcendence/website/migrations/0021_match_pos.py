# Generated by Django 4.2 on 2024-01-17 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0020_tournament_is_started'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='pos',
            field=models.CharField(blank=True, choices=[('top', 'Top'), ('bottom', 'Bottom')], max_length=6, null=True),
        ),
    ]
