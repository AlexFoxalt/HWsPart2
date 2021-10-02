from django.db import models


# Create your models here.

class Teacher(models.Model):
    name = models.CharField(max_length=30, null=False)
    surname = models.CharField(max_length=30, null=False)
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", null=True, default='-')
    time_create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
