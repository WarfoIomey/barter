# Generated by Django 4.2 on 2025-04-15 02:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ad',
            name='image',
            field=models.ImageField(blank=True, upload_to='ad_images', verbose_name='Фото'),
        ),
    ]
