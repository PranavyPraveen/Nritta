# Generated by Django 5.0.4 on 2024-07-12 06:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Homeapp', '0016_paymentamount_course'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paymentamount',
            name='course',
        ),
    ]
