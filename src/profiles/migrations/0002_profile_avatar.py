# Generated by Django 2.2.2 on 2019-06-26 00:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='avatar',
            field=models.CharField(default='img/avatars/tom.jpg', max_length=260),
        ),
    ]
