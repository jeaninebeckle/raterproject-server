# Generated by Django 3.1.3 on 2020-11-29 21:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('raterprojectapi', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='review',
            old_name='game',
            new_name='game_id',
        ),
        migrations.RenameField(
            model_name='review',
            old_name='player',
            new_name='player_id',
        ),
    ]