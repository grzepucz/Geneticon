# Generated by Django 3.1.3 on 2020-11-08 21:21

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geneticon', '0008_auto_20201108_2121'),
    ]

    operations = [
        migrations.AlterField(
            model_name='population',
            name='create_date',
            field=models.DateField(default=datetime.datetime(2020, 11, 8, 21, 21, 31, 22437)),
        ),
    ]
