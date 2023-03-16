# Generated by Django 4.1.3 on 2023-02-23 13:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('flipkart_api', '0001_initial'),
        ('flipkart_app', '0002_order_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='city',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='phone_number',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='flipkart_api.product'),
        ),
        migrations.AddField(
            model_name='order',
            name='state',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='zipcode',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.RemoveField(
            model_name='order',
            name='address',
        ),
        migrations.DeleteModel(
            name='Address',
        ),
        migrations.AddField(
            model_name='order',
            name='address',
            field=models.CharField(max_length=50, null=True),
        ),
    ]