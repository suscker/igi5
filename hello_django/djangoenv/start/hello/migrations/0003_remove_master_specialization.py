# Generated by Django 5.0.6 on 2024-05-22 19:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0002_alter_master_specialization_alter_part_car_model_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='master',
            name='specialization',
        ),
    ]
