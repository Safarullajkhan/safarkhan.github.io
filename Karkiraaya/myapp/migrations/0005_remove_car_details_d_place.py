# Generated by Django 4.1.7 on 2023-06-21 05:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_remove_car_details_d_time_alter_car_details_d_place'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='car_details',
            name='d_place',
        ),
    ]