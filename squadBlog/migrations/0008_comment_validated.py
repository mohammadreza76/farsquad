# Generated by Django 3.1.6 on 2021-05-25 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('squadBlog', '0007_auto_20210525_1145'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='validated',
            field=models.CharField(default='no', max_length=5),
        ),
    ]
