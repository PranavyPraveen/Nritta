# Generated by Django 5.0.4 on 2024-07-10 06:50

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Homeapp', '0013_alter_paymentdetails_amount'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paymentdetails',
            name='amount',
        ),
        migrations.CreateModel(
            name='PaymentAmount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField()),
                ('start_date', models.DateField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='paymentdetails',
            name='amount',
            field=models.ManyToManyField(to='Homeapp.paymentamount'),
        ),
    ]
