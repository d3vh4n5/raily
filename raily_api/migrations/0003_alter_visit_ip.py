# Generated by Django 5.0.2 on 2024-03-05 20:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('raily_api', '0002_visit_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visit',
            name='ip',
            field=models.CharField(max_length=20),
        ),
    ]
