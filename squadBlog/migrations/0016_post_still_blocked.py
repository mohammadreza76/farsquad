# Generated by Django 3.1.6 on 2021-09-13 08:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('squadBlog', '0015_remove_post_duration'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='still_blocked',
            field=models.BooleanField(default=False),
        ),
    ]