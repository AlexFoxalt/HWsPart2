# Generated by Django 3.2.7 on 2021-11-03 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='filled',
            field=models.BooleanField(default=False),
        ),
    ]