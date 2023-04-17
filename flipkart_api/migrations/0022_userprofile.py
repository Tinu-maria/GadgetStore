# Generated by Django 4.1.3 on 2023-03-29 07:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import flipkart_api.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('flipkart_api', '0021_alter_category_unique_together'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, upload_to=flipkart_api.models.profile_path_handler)),
                ('phone', models.PositiveIntegerField(blank=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]