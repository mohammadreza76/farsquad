# Generated by Django 3.1.6 on 2021-05-01 13:35

import accounts.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='profiles/default.png', upload_to=accounts.models.upload_to, verbose_name='Image'),
        ),
    ]
