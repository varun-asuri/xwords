# Generated by Django 2.2.10 on 2020-05-13 22:25

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crosswords', '0002_auto_20200513_1723'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dictionary',
            name='characters',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=1), blank=True, default=list, size=None),
        ),
    ]
