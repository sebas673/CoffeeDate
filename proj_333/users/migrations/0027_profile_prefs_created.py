# Generated by Django 2.1.7 on 2019-05-01 06:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0026_profile_prefs_match'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='prefs_created',
            field=models.BooleanField(default=False),
        ),
    ]
