# Generated by Django 2.1.2 on 2020-01-31 08:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('heartbeat', '0002_auto_20200131_0355'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='heartbeatconfig',
            name='instances',
        ),
    ]
