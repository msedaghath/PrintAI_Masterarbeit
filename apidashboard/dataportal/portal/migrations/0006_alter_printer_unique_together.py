# Generated by Django 4.1.4 on 2023-07-11 08:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0005_dataprint_printer_printer_profile'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='printer',
            unique_together={('ip_address', 'api_key')},
        ),
    ]
