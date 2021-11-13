# Generated by Django 3.2.7 on 2021-11-10 11:51

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('person_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='users.person')),
                ('photo', models.ImageField(default='default_avatar/teacher_avatar.png', upload_to='user_photo/teacher/', verbose_name='Photo')),
                ('date_of_employment', models.DateField(default=datetime.datetime.now, null=True, verbose_name='Date of employment')),
                ('experience_in_years', models.IntegerField(default=0, null=True, verbose_name='Experience in years')),
                ('courses', models.ManyToManyField(to='users.Course', verbose_name='Course')),
            ],
            options={
                'verbose_name': 'Преподаватель',
                'verbose_name_plural': 'Преподаватели',
            },
            bases=('users.person',),
        ),
    ]
