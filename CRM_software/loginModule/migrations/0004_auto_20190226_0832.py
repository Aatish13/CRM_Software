# Generated by Django 2.1.7 on 2019-02-26 03:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loginModule', '0003_usertype'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usertype',
            name='user',
        ),
        migrations.AddField(
            model_name='usertype',
            name='user_name',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
