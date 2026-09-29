import json
from rest_framework import serializers
from .models import Robotti

class RobottiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Robotti
        fields = ['id', 'modelname', 'serialnumber', 'location_x', 'location_y']

