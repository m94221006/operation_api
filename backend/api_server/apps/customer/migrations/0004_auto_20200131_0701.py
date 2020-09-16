# Generated by Django 2.1.2 on 2020-01-31 07:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0003_auto_20200131_0640'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='relate_to_customer', to='customer.CustomerInfo'),
        ),
    ]
