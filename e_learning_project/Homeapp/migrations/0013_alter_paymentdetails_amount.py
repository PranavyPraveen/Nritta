# Generated by Django 5.0.4 on 2024-07-10 06:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Homeapp', '0012_paymentdetails'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentdetails',
            name='amount',
            field=models.FloatField(null=True),
        ),
    ]
