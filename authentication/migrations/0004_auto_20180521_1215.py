# Generated by Django 2.0.4 on 2018-05-21 06:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_auto_20180512_1841'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='reputaion',
        ),
        migrations.AddField(
            model_name='user',
            name='is_verified',
            field=models.BooleanField(default=False),
        ),
    ]