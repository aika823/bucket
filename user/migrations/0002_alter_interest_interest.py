# Generated by Django 3.2.9 on 2021-11-06 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interest',
            name='interest',
            field=models.CharField(max_length=10, unique=True),
        ),
    ]
