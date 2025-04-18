# Generated by Django 4.2 on 2025-04-16 05:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ads', '0003_alter_ad_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ad',
            name='user',
            field=models.ForeignKey(help_text='Укажите пользователя', on_delete=django.db.models.deletion.CASCADE, related_name='ads', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
    ]
