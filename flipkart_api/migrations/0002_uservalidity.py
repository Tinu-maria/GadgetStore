# Generated by Django 4.1.3 on 2023-02-13 08:48

from django.db import migrations, models
import django_fsm


class Migration(migrations.Migration):

    dependencies = [
        ('flipkart_api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserValidity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', django_fsm.FSMField(default='active', max_length=50)),
                ('name', models.CharField(max_length=10)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
