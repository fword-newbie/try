# Generated by Django 3.2.9 on 2021-11-12 05:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0004_auto_20211112_0526'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='people',
            name='address',
        ),
        migrations.RemoveField(
            model_name='people',
            name='badge',
        ),
        migrations.RemoveField(
            model_name='people',
            name='birthday',
        ),
        migrations.RemoveField(
            model_name='people',
            name='emailcheck',
        ),
        migrations.RemoveField(
            model_name='people',
            name='emailcheckcode',
        ),
        migrations.RemoveField(
            model_name='people',
            name='fb_id',
        ),
        migrations.RemoveField(
            model_name='people',
            name='fcm_id',
        ),
        migrations.RemoveField(
            model_name='people',
            name='gender',
        ),
        migrations.RemoveField(
            model_name='people',
            name='group',
        ),
        migrations.RemoveField(
            model_name='people',
            name='height',
        ),
        migrations.RemoveField(
            model_name='people',
            name='must_change_password',
        ),
        migrations.RemoveField(
            model_name='people',
            name='name',
        ),
        migrations.RemoveField(
            model_name='people',
            name='status',
        ),
        migrations.RemoveField(
            model_name='people',
            name='token',
        ),
        migrations.RemoveField(
            model_name='people',
            name='verified',
        ),
        migrations.RemoveField(
            model_name='people',
            name='weight',
        ),
    ]
