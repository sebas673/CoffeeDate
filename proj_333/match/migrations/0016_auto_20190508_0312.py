# Generated by Django 2.1.7 on 2019-05-08 03:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('match', '0015_auto_20190508_0300'),
    ]

    operations = [
        migrations.AddField(
            model_name='pair',
            name='pair1_image',
            field=models.ImageField(default='default.jpg', upload_to='group_pics'),
        ),
        migrations.AddField(
            model_name='pair',
            name='pair2_image',
            field=models.ImageField(default='default.jpg', upload_to='group_pics'),
        ),
    ]