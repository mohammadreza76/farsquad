# Generated by Django 3.1.6 on 2021-05-01 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_profile_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='email',
            field=models.EmailField(max_length=60, null=True),
        ),
    ]
