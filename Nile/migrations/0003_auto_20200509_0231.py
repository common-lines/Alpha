# Generated by Django 3.0.5 on 2020-05-08 23:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Nile', '0002_contact'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='phone',
            field=models.CharField(default='00-000-000-000', max_length=255, null=True),
        ),
    ]