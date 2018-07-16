# Generated by Django 2.0.6 on 2018-07-16 08:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('designer', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deck',
            name='back_border_color',
        ),
        migrations.RemoveField(
            model_name='deck',
            name='front_border_color',
        ),
        migrations.RemoveField(
            model_name='deck',
            name='icon',
        ),
        migrations.RemoveField(
            model_name='deck',
            name='same_reverse',
        ),
        migrations.RemoveField(
            model_name='game',
            name='icon',
        ),
        migrations.AlterField(
            model_name='deck',
            name='size',
            field=models.CharField(choices=[('SE', 'standard euro'), ('ME', 'mini euro'), ('SA', 'standard american'), ('MA', 'mini american')], max_length=1),
        ),
    ]