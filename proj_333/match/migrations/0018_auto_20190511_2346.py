# Generated by Django 2.1.7 on 2019-05-11 23:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('match', '0017_auto_20190508_0531'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='group_image',
            field=models.ImageField(default='default.jpg', upload_to='profile_pics'),
        ),
    ]