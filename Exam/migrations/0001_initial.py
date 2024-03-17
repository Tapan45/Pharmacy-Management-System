# Generated by Django 4.2.6 on 2024-02-13 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Medicine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('medicine_id', models.CharField(max_length=255)),
                ('medicine_name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('manufacturing_date', models.DateField()),
                ('expire_date', models.DateField()),
                ('quantity', models.IntegerField()),
                ('selling_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('discounted_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('medicine_image', models.ImageField(upload_to='medicine_images/')),
            ],
        ),
    ]