# Generated by Django 3.1.6 on 2021-05-19 08:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0017_profile_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='score',
        ),
        migrations.AddField(
            model_name='user',
            name='mohaverh_score',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='overall_score',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='squad_score',
            field=models.IntegerField(default=0),
        ),
    ]
