# Generated by Django 3.2.9 on 2021-11-18 06:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0046_auto_20211118_0619'),
    ]

    operations = [
        migrations.RenameField(
            model_name='uid_id_friend',
            old_name='user_id',
            new_name='my_id',
        ),
        migrations.RemoveField(
            model_name='uid_id_friend',
            name='friend_name',
        ),
        migrations.RemoveField(
            model_name='uid_id_friend',
            name='list_id',
        ),
    ]