from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns
from ride.api import views


urlpatterns = patterns('',
    url(r'^$', views.api_root),
    url(r'^users/$', views.UserList.as_view(), name="user-list"),
    url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view(), name="user-detail"),
    url(r'^routes/$', views.RouteList.as_view(), name="route-list"),
    url(r'^routes/(?P<pk>[0-9]+)/$', views.RouteDetail.as_view(), name="route-detail"),
    url(r'^vehicles/$', views.VehicleList.as_view(), name="vehicle-list"),
    url(r'^vehicles/(?P<pk>[0-9]+)/$', views.VehicleDetail.as_view(), name="vehicle-detail"),
    url(r'^rides/$', views.RideList.as_view(), name="ride-list"),
)

urlpatterns = format_suffix_patterns(urlpatterns)
