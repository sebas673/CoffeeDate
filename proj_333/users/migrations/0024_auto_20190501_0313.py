# Generated by Django 2.1.7 on 2019-05-01 03:13

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0023_auto_20190501_0310'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Characteristics',
            new_name='Prefs',
        ),
    ]