# Generated by Django 3.1.7 on 2021-04-29 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0028_auto_20210429_0812'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='admin',
            field=models.BooleanField(default=False),
        ),
    ]
