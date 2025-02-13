# Generated by Django 5.0.2 on 2024-03-02 18:09

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailer', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ApiKey',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=150, verbose_name='Value')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='apiKey', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
        ),
    ]
