# Generated by Django 3.0.5 on 2020-05-16 20:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Nile', '0011_auto_20200516_1306'),
    ]

    operations = [
        migrations.CreateModel(
            name='Substitute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seller', models.BooleanField(default=False)),
                ('received', models.BooleanField(default=False)),
                ('refund', models.BooleanField(default=False)),
                ('delivered', models.BooleanField(default=False)),
                ('stipulate', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Nile.Stipulate')),
            ],
        ),
    ]
