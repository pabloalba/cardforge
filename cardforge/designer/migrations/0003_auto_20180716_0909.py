# Generated by Django 2.0.6 on 2018-07-16 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('designer', '0002_auto_20180716_0838'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deck',
            name='size',
            field=models.CharField(choices=[('SE', 'standard euro'), ('ME', 'mini euro'), ('SA', 'standard american'), ('MA', 'mini american')], max_length=2),
        ),
    ]
