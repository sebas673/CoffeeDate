# Generated by Django 2.1.7 on 2019-05-08 02:13

import django.contrib.auth.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('match', '0013_auto_20190508_0211'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='members',
            field=models.ManyToManyField(default=django.contrib.auth.models.User, to='users.Profile'),
        ),
    ]