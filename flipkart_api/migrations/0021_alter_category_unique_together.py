# Generated by Django 4.1.3 on 2023-03-28 15:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flipkart_api', '0020_rename_category_category_category_name'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='category',
            unique_together={('product', 'category_name')},
        ),
    ]
