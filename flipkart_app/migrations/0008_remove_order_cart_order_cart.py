# Generated by Django 4.1.3 on 2023-03-02 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flipkart_app', '0007_order_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='cart',
        ),
        migrations.AddField(
            model_name='order',
            name='cart',
            field=models.ManyToManyField(null=True, to='flipkart_app.cart'),
        ),
    ]
