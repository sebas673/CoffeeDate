# Generated by Django 2.1.7 on 2019-05-08 03:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('match', '0014_auto_20190508_0213'),
    ]

    operations = [
        migrations.AddField(
            model_name='pair',
            name='pair1_email',
            field=models.CharField(default='princeton@princeton.edu', max_length=50),
        ),
        migrations.AddField(
            model_name='pair',
            name='pair2_email',
            field=models.CharField(default='princeton@princeton.edu', max_length=50),
        ),
        migrations.AlterField(
            model_name='group',
            name='members',
            field=models.ManyToManyField(to='users.Profile'),
        ),
    ]
