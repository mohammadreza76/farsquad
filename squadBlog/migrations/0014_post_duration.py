# Generated by Django 3.1.6 on 2021-09-13 06:22

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('squadBlog', '0013_auto_20210912_1533'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='duration',
            field=models.DurationField(default=datetime.timedelta, null=True),
        ),
    ]