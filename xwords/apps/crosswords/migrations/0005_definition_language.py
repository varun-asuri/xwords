# Generated by Django 2.2.10 on 2020-05-13 22:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crosswords', '0004_auto_20200513_1744'),
    ]

    operations = [
        migrations.AddField(
            model_name='definition',
            name='language',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='crosswords.Dictionary'),
        ),
    ]