# Generated by Django 5.2 on 2025-04-21 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0003_remove_servicerequest_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='servicerequest',
            name='created_at',
        ),
        migrations.AlterField(
            model_name='servicerequest',
            name='full_name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='servicerequest',
            name='service_type',
            field=models.CharField(max_length=50),
        ),
    ]
