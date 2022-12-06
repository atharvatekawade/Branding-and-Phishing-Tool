from django.db import models

# Create your models here.

class Verify(models.Model):
    url=models.CharField(max_length=250)
    identity=models.CharField(max_length=10,default='0000000000')

    def __str__(self):
        return self.url + '-' +  self.identity

class Report(models.Model):
    url=models.CharField(max_length=250)
    #identity=models.CharField(max_length=10,default='0000000000')
    updated=models.CharField(max_length=20)
    count=models.IntegerField()

    def __str__(self):
        return self.url + '-' +  self.updated
