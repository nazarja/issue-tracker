# Generated by Django 2.2.2 on 2019-06-27 22:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.CharField(default='/static/img/avatars/violet.jpeg', max_length=260),
        ),
    ]