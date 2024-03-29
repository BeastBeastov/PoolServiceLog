# Generated by Django 5.0.2 on 2024-03-08 20:58

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poolservice', '0008_poolservice_author'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='pool',
            name='owner',
            field=models.CharField(max_length=255, verbose_name='Владелец'),
        ),
        migrations.AlterField(
            model_name='poolservice',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Исполнитель'),
        ),
    ]
