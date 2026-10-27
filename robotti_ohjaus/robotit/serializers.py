from django.db import transaction
from rest_framework import serializers
from .models import Location, Robotti


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id', 'location_x', 'location_y']


class RobottiSerializer(serializers.ModelSerializer):
    location_x = serializers.FloatField(required=False, allow_null=True, write_only=True)
    location_y = serializers.FloatField(required=False, allow_null=True, write_only=True)
    locations = LocationSerializer(many=True, read_only=True)

    class Meta:
        model = Robotti
        fields = ['id', 'modelname', 'serialnumber', 'location_x', 'location_y', 'locations']
        validators = []

    @transaction.atomic
    def create(self, validated_data):
        location_x = validated_data.pop('location_x', None)
        location_y = validated_data.pop('location_y', None)
        robotti, _ = Robotti.objects.get_or_create(**validated_data)

        if location_x is not None or location_y is not None:
            Location.objects.create(
                robotti=robotti,
                location_x=location_x,
                location_y=location_y,
            )

        return robotti

    @transaction.atomic
    def update(self, instance, validated_data):
        location_x = validated_data.pop('location_x', None)
        location_y = validated_data.pop('location_y', None)
        instance = super().update(instance, validated_data)

        if location_x is not None or location_y is not None:
            Location.objects.create(
                robotti=instance,
                location_x=location_x,
                location_y=location_y,
            )

        return instance
