# Generated by Django 2.2.2 on 2019-07-09 02:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.CharField(default='/static/img/avatars/paula.jpg', max_length=260),
        ),
    ]
