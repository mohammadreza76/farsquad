# Generated by Django 3.1.6 on 2021-05-01 13:18

import accounts.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_auto_20210430_1902'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='profiles/default.jpg', upload_to=accounts.models.upload_to, verbose_name='Image'),
        ),
    ]
