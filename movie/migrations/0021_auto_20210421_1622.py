# Generated by Django 3.1.4 on 2021-04-21 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0020_remove_category_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Категория'),
        ),
        migrations.AlterField(
            model_name='category',
            name='name_en',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Категория'),
        ),
        migrations.AlterField(
            model_name='category',
            name='name_kk',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Категория'),
        ),
        migrations.AlterField(
            model_name='category',
            name='name_ru',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Категория'),
        ),
    ]
