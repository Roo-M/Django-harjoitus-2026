from django.db import models


class Robotti(models.Model):
  modelname = models.CharField(max_length=255)
  serialnumber = models.CharField(max_length=255)

  class Meta:
    constraints = [
      models.UniqueConstraint(
        fields=['modelname', 'serialnumber'],
        name='unique_robotti_model_serialnumber',
      ),
    ]

class Location(models.Model):
  robotti = models.ForeignKey(Robotti, on_delete=models.CASCADE, related_name='locations')
  location_x = models.FloatField(null=True, blank=True)
  location_y = models.FloatField(null=True, blank=True)
