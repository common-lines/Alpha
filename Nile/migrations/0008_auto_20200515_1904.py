# Generated by Django 3.0.5 on 2020-05-15 16:04

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Nile', '0007_store_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='stipulate',
            name='accepted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='stipulate',
            name='charge',
            field=models.FloatField(default=5.0),
        ),
        migrations.AddField(
            model_name='stipulate',
            name='reference',
            field=models.CharField(default='None', max_length=250, unique=True),
        ),
        migrations.AddField(
            model_name='stipulate',
            name='shipping',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='stipulate',
            name='slot',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
