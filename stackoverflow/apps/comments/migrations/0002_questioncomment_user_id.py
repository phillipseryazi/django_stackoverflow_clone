# Generated by Django 2.2.3 on 2019-07-13 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='questioncomment',
            name='user_id',
            field=models.IntegerField(default=0),
        ),
    ]