# Generated by Django 4.2.6 on 2024-02-20 17:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Exam', '0005_medicine_category_medicine_subcategory'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sales',
            name='address',
        ),
        migrations.RemoveField(
            model_name='sales',
            name='state',
        ),
        migrations.RemoveField(
            model_name='sales',
            name='zipcode',
        ),
    ]
