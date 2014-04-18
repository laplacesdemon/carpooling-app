from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from ride.api.serializers import (
    UserSerializer,
    RouteSerializer,
    RideBriefSerializer,
    VehicleSerializer,
)
from ride.models import (
    Route,
    RideAdvert,
    Vehicle,
)


@api_view(('GET',))
def api_root(request, format=None):
    """Api endpoint"""
    return Response({
        'routes': reverse('route-list', request=request, format=format),
        'rides': reverse('ride-list', request=request, format=format),
    })


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class RouteList(generics.ListCreateAPIView):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer


class RouteDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer


class VehicleList(generics.ListCreateAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer


class VehicleDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer


class RideList(APIView):

    def get(self, request, format=None):
        """returns all rides for certain criteria"""
        rides = RideAdvert.objects.rides()
        serializer = RideBriefSerializer(rides, many=True)
        return Response(serializer.data)
