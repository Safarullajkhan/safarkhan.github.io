# Generated by Django 4.1.7 on 2023-06-23 04:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0007_deliveryandreturn_fdate_deliveryandreturn_license_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deliveryandreturn',
            name='fdate',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='deliveryandreturn',
            name='rdate',
            field=models.DateField(null=True),
        ),
    ]
