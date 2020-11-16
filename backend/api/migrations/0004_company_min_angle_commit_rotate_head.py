# Generated by Django 3.1.3 on 2020-11-15 23:51

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20201115_1552'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='min_angle_commit_rotate_head',
            field=models.SmallIntegerField(default=40, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(90)], verbose_name='Minimum angle to commit rotate head'),
        ),
    ]