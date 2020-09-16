# Generated by Django 2.1.2 on 2020-03-17 07:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('alert', '0001_initial'),
        ('customer', '0005_auto_20200131_0708'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerContact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipient_id', models.CharField(db_column='recipient_id', max_length=50)),
                ('subject', models.CharField(blank=True, default=None, max_length=50, null=True)),
                ('cid', models.ForeignKey(db_column='cid', on_delete=django.db.models.deletion.CASCADE, to='customer.CustomerInfo')),
                ('type_id', models.ForeignKey(db_column='type_id', on_delete=django.db.models.deletion.CASCADE, to='alert.AlertNotifyType')),
            ],
            options={
                'db_table': 'customer_contact',
            },
        ),
    ]