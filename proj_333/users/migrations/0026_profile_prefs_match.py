# Generated by Django 2.1.7 on 2019-05-01 06:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0025_auto_20190501_0341'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='prefs_match',
            field=models.BooleanField(default=False),
        ),
    ]