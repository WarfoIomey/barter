# Generated by Django 4.2 on 2025-04-15 05:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0002_ad_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ad',
            name='image',
            field=models.ImageField(blank=True, upload_to='images', verbose_name='Фото'),
        ),
    ]
