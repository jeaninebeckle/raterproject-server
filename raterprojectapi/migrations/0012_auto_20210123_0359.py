# Generated by Django 3.1.3 on 2021-01-23 03:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('raterprojectapi', '0011_remove_game_action_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='categories',
            field=models.ManyToManyField(related_name='game_categories', related_query_name='game_category', to='raterprojectapi.Categories'),
        ),
    ]
