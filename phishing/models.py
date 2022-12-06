from django.db import models

# Create your models here.

class Fraud(models.Model):
    url=models.CharField(max_length=250)

    def __str__(self):
        return self.url
