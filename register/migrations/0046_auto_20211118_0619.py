# Generated by Django 3.2.9 on 2021-11-18 06:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0045_uid_id_friend_friend_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='uid_id_friend',
            name='friend_id',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='uid_id_friend',
            name='relation_type',
            field=models.CharField(max_length=3, null=True),
        ),
    ]
