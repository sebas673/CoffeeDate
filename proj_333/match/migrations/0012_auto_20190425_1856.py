# Generated by Django 2.1.7 on 2019-04-25 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('match', '0011_auto_20190424_0615'),
    ]

    operations = [
        migrations.AddField(
            model_name='pair',
            name='pair_1_first',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='pair',
            name='pair_1_last',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='pair',
            name='pair_2_first',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='pair',
            name='pair_2_last',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
