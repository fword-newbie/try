# Generated by Django 3.2.9 on 2021-11-17 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0041_alter_record_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
