# Generated by Django 3.2 on 2021-05-31 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_auto_20210530_1843'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='url',
            name='ip',
        ),
        migrations.RemoveField(
            model_name='url',
            name='up',
        ),
        migrations.AddField(
            model_name='url',
            name='score',
            field=models.IntegerField(default=0),
        ),
    ]
