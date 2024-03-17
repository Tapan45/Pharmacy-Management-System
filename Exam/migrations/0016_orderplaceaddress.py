# Generated by Django 4.2.6 on 2024-03-13 22:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Exam', '0015_rename_total_amount_payment_amount_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderPlaceAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=15)),
                ('phone', models.CharField(blank=True, max_length=15)),
                ('state', models.CharField(blank=True, max_length=255)),
                ('address', models.TextField(blank=True)),
                ('zipcode', models.CharField(blank=True, max_length=10)),
                ('user_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Exam.userprofile')),
            ],
        ),
    ]
