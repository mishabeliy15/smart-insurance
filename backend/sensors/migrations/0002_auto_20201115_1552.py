# Generated by Django 3.1.3 on 2020-11-15 13:52

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sensors', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sensor',
            name='created',
            field=models.DateTimeField(auto_now_add=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='speedrecord',
            name='created',
            field=models.DateTimeField(auto_now_add=True, db_index=True),
        ),
        migrations.CreateModel(
            name='HeadRotateRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('angle', models.SmallIntegerField(db_index=True, editable=False, validators=[django.core.validators.MinValueValidator(-360), django.core.validators.MaxValueValidator(360)], verbose_name='Rotate head angle')),
                ('sensor', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='sensors.sensor', verbose_name='Sensor')),
                ('speed', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='sensors.speedrecord', verbose_name='Speed')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
