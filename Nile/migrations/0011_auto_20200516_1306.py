# Generated by Django 3.0.5 on 2020-05-16 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Nile', '0010_auto_20200515_1945'),
    ]

    operations = [
        migrations.AddField(
            model_name='stipulate',
            name='admin',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='stipulate',
            name='payment',
            field=models.BooleanField(default=False),
        ),
    ]
