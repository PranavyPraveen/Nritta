# Generated by Django 5.0.4 on 2024-05-08 05:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Homeapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='register',
            name='gender',
            field=models.CharField(choices=[('none', 'None'), ('other', 'Other'), ('male', 'Male'), ('female', 'Female')], default='none', help_text='Enter your gender', max_length=20),
        ),
    ]
