# Generated by Django 2.1.7 on 2019-05-08 02:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0027_profile_prefs_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prefs',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Prefs', to=settings.AUTH_USER_MODEL),
        ),
    ]