# Generated by Django 2.2.2 on 2019-06-29 17:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0004_ticket_avatar'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticket',
            name='view_count',
        ),
    ]