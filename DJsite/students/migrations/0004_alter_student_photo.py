# Generated by Django 3.2.7 on 2021-11-05 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0003_alter_student_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='photo',
            field=models.ImageField(default='default_avatar/student_avatar3.png', upload_to='user_photo/student/', verbose_name='Photo'),
        ),
    ]