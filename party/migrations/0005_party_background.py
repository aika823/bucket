# Generated by Django 3.2.9 on 2021-12-02 01:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('party', '0004_party_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='party',
            name='background',
            field=models.ImageField(default='default_image.jpg', upload_to='party/'),
        ),
    ]
