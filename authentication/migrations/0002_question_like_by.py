# Generated by Django 2.0.4 on 2018-05-11 08:15

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='like_by',
            field=models.ManyToManyField(related_name='user', to=settings.AUTH_USER_MODEL),
        ),
    ]