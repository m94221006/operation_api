# Generated by Django 2.1.2 on 2020-01-31 03:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('heartbeat', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='heartbeatconfig',
            name='created_by',
            field=models.CharField(default='system', max_length=50),
        ),
        migrations.AlterField(
            model_name='heartbeatconfig',
            name='updated_by',
            field=models.CharField(default='system', max_length=50),
        ),
    ]
