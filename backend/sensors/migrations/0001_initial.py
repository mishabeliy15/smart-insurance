# Generated by Django 3.1.3 on 2020-11-08 23:27

from django.conf import settings
import django.contrib.gis.db.models.fields
import django.core.validators
from django.contrib.postgres.operations import CreateExtension
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        CreateExtension('postgis'),
        migrations.CreateModel(
            name='Sensor',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('uuid', models.UUIDField(db_index=True, editable=False, primary_key=True, serialize=False, unique=True, verbose_name='UUID')),
                ('sensor_type', models.PositiveSmallIntegerField(choices=[(1, 'SPEED'), (2, 'HEAD_ANGLE')], editable=False, verbose_name='Sensor type')),
                ('owner', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Owner')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SpeedRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('speed', models.FloatField(editable=False, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(400)], verbose_name='Speed')),
                ('over_speed', models.FloatField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='Over speed')),
                ('location', django.contrib.gis.db.models.fields.PointField(editable=False, geography=True, srid=4326, verbose_name='Location')),
                ('sensor', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='sensors.sensor', verbose_name='Sensor')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]