# Generated by Django 2.0.4 on 2018-05-09 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0008_user_staff'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='staff',
            field=models.NullBooleanField(default=False),
        ),
    ]