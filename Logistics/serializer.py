from rest_framework import serializers

from Logistics.models import Location



class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ("location","price",)