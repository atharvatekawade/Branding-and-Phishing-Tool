# Generated by Django 3.2 on 2021-05-30 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_auto_20210522_1037'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='url',
            name='score',
        ),
        migrations.AddField(
            model_name='url',
            name='ip',
            field=models.CharField(default='NA', max_length=250),
        ),
        migrations.AddField(
            model_name='url',
            name='up',
            field=models.CharField(default='NA', max_length=20),
        ),
    ]
