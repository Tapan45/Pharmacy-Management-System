# Generated by Django 4.2.6 on 2024-03-14 21:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Exam', '0021_alter_address_name_alter_address_phone_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='payment_date',
        ),
    ]
