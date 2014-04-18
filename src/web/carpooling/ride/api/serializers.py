from django.contrib.auth.models import User
from rest_framework import serializers
from ride.models import (
    Route,
    Vehicle,
)


class UserSerializer(serializers.HyperlinkedModelSerializer):
    public_name = serializers.CharField(source='public_name')

    class Meta:
        model = User
        fields = ('url', 'username', 'public_name', )


class RouteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Route
        fields = ('start_latitude', 'start_longitude', 'start_radius', 'start_address',
                  'end_latitude', 'end_longitude', 'end_radius', 'end_address')


class RouteBriefSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Route
        fields = ('start_address',
                  'end_address')


class VehicleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Vehicle


class RideBriefSerializer(serializers.Serializer):
    pk = serializers.Field()
    route = RouteBriefSerializer()
    driver = UserSerializer()
    vehicle = VehicleSerializer()
    registered_seats = serializers.CharField(min_length=3, max_length=10)
    price = serializers.IntegerField()
    date = serializers.DateTimeField()
