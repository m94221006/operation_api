# Generated by Django 2.1.2 on 2020-01-31 06:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0002_auto_20200131_0355'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customerinstance',
            name='cid',
        ),
        migrations.RemoveField(
            model_name='customerinstance',
            name='instance',
        ),
        migrations.DeleteModel(
            name='CustomerInstance',
        ),
    ]
