from rest_framework import serializers as s

from ads.models import Location


class LocationSerializer(s.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'
