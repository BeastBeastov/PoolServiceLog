# Generated by Django 5.0.2 on 2024-02-28 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poolservice', '0006_pool_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pool',
            name='phone',
            field=models.CharField(blank=True, max_length=20, verbose_name='Телефон'),
        ),
    ]
