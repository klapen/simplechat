# Generated by Django 2.2.1 on 2019-05-24 19:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_remove_message_cindex'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='room',
            field=models.CharField(default='no-room', max_length=100),
        ),
    ]
