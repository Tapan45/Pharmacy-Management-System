# Generated by Django 4.2.6 on 2024-03-15 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Exam', '0026_alter_paymentamount_mrp_total'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentamount',
            name='additional_discount',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='paymentamount',
            name='total_amount',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='paymentamount',
            name='total_payable',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='paymentamount',
            name='total_savings',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
    ]
