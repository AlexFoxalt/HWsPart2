# Generated by Django 3.2.7 on 2021-11-03 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='photo',
            field=models.ImageField(default='default_avatar/student_avatar9.png', upload_to='user_photo/student/', verbose_name='Photo'),
        ),
    ]