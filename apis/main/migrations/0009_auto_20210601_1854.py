# Generated by Django 3.2.3 on 2021-06-01 18:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_auto_20210531_1850'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Fraud',
        ),
        migrations.DeleteModel(
            name='Report',
        ),
        migrations.DeleteModel(
            name='Url',
        ),
        migrations.DeleteModel(
            name='Verify',
        ),
    ]
