# Generated by Django 2.2.2 on 2019-07-03 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0018_auto_20190703_2000'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.CharField(default='/static/img/avatars/molly.png', max_length=260),
        ),
    ]