# Generated by Django 3.1.6 on 2021-09-12 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('squadBlog', '0011_post_start_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='start_time',
            field=models.DateField(auto_now=True, null=True),
        ),
    ]
