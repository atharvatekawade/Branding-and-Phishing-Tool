from django.db import models

# Create your models here.

class Person(models.Model):
    identity=models.CharField(max_length=10)
    updated=models.CharField(max_length=20)
    count=models.IntegerField()
    category=models.CharField(max_length=10,default='branding')

    def __str__(self):
        return self.id

