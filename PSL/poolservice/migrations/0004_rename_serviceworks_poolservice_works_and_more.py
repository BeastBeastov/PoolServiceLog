# Generated by Django 5.0.2 on 2024-02-26 20:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poolservice', '0003_alter_pool_year_create'),
    ]

    operations = [
        migrations.RenameField(
            model_name='poolservice',
            old_name='serviceworks',
            new_name='works',
        ),
        migrations.AlterField(
            model_name='poolservice',
            name='pool',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='poolservice.pool', verbose_name='Бассейн'),
        ),
    ]
