# Generated by Django 2.1.7 on 2019-04-14 03:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20190414_0249'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='is_matched',
            field=models.BooleanField(default=False),
        ),
    ]