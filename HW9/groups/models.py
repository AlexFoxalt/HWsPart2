from django.db import models


# Create your models here.

class Group (models.Model):
    name = models.CharField(max_length=30, null=False)
    faculty = models.CharField(max_length=30, null=False)
    course = models.IntegerField(null=True, default=1)
    headman = models.CharField(max_length=50, null=True, default='-')
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", null=True, default='-')
    time_create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
