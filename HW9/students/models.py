from django.db import models
from datetime import datetime


# Create your models here.

class Student(models.Model):
    name = models.CharField(max_length=100, null=False)
    city = models.CharField(max_length=30, null=False)
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", null=True, default='-')
    time_create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        data = self.name, self.city, self.time_create.strftime("%m %B%Y, %H:%M:%S")
        return ' --- '.join(data)