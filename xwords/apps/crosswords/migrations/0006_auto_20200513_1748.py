# Generated by Django 2.2.10 on 2020-05-13 22:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crosswords', '0005_definition_language'),
    ]

    operations = [
        migrations.AlterField(
            model_name='definition',
            name='language',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crosswords.Dictionary'),
        ),
    ]
