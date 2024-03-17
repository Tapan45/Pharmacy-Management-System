# Generated by Django 4.2.6 on 2024-02-20 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Exam', '0006_remove_sales_address_remove_sales_state_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='sales',
            name='address',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='sales',
            name='state',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='sales',
            name='zipcode',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='medicine',
            name='category',
            field=models.CharField(blank='True', choices=[('wellness', 'Wellness'), ('beauty', 'Beauty')], max_length=20),
        ),
    ]