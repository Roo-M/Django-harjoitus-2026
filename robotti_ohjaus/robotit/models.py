from django.db import models

class Robotti(models.Model):
  robotType = models.CharField(max_length=255)
  robotModel = models.CharField(max_length=255)
  robotIDnumber = models.IntegerField(null=True)
  added_date = models.DateField(null=True)