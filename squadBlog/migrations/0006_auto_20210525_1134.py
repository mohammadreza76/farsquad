# Generated by Django 3.1.6 on 2021-05-25 07:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('squadBlog', '0005_post_blocked_by_person_for_answering'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='stop_showing',
            new_name='stop_showing_temporary',
        ),
    ]