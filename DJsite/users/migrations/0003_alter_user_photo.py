# Generated by Django 3.2.7 on 2021-10-23 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='photo',
            field=models.ImageField(default='default_avatar.png', upload_to='user_photo', verbose_name='Photo'),
        ),
    ]