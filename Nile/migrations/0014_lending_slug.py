# Generated by Django 3.0.5 on 2020-05-20 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Nile', '0013_lending'),
    ]

    operations = [
        migrations.AddField(
            model_name='lending',
            name='slug',
            field=models.SlugField(default='Chat-With-Robot', unique=True),
        ),
    ]
