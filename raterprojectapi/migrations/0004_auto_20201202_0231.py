# Generated by Django 3.1.3 on 2020-12-02 02:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('raterprojectapi', '0003_auto_20201201_0243'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='game_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', related_query_name='review', to='raterprojectapi.game'),
        ),
    ]
