# Generated by Django 4.2.6 on 2024-03-04 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Exam', '0010_holiday'),
    ]

    operations = [
        migrations.CreateModel(
            name='LabBooking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('patient_name', models.CharField(max_length=50)),
                ('patient_mobile', models.CharField(max_length=10)),
                ('patient_pincode', models.CharField(max_length=6)),
                ('lab_test', models.CharField(max_length=255)),
                ('terms_agreed', models.BooleanField()),
            ],
        ),
    ]
