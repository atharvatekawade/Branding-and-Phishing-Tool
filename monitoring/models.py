from django.db import models

# Create your models here.

class Url(models.Model):
    main=models.CharField(max_length=250)
    similar=models.CharField(max_length=250)
    score=models.CharField(max_length=20,default='0')
    updated=models.CharField(max_length=20)

    def __str__(self):
        return self.main + '-' +  self.similar





