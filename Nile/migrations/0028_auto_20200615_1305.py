# Generated by Django 3.0.5 on 2020-06-15 10:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Nile', '0027_center_explore'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='center',
            name='detail',
        ),
        migrations.RemoveField(
            model_name='center',
            name='phone3',
        ),
    ]