# Generated by Django 3.2.7 on 2021-11-03 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_filled'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='filled',
            field=models.BooleanField(default=False, verbose_name='Filled information status'),
        ),
    ]