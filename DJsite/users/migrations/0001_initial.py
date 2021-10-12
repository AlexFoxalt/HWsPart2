# Generated by Django 3.2.7 on 2021-10-12 08:37

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('birthday', models.DateField()),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone_number', models.CharField(max_length=50, unique=True)),
                ('faculty', models.CharField(default='not chosen', max_length=255)),
                ('position', models.CharField(default='not chosen', max_length=255)),
                ('time_create', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='users.user')),
                ('previous_educational_institution', models.CharField(default='-', max_length=100, null=True)),
            ],
            bases=('users.user',),
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='users.user')),
                ('date_of_employment', models.DateField(default=datetime.datetime.now, null=True)),
                ('experience_in_years', models.IntegerField(default=0, null=True)),
            ],
            bases=('users.user',),
        ),
    ]