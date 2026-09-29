from django.db import models


class Robotti(models.Model):
  modelname = models.CharField(max_length=255)
  serialnumber = models.CharField(max_length=255)
  location_x = models.FloatField(null=True, blank=True)
  location_y = models.FloatField(null=True, blank=True)
