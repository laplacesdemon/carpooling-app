from django.test import TestCase
from django.contrib.auth.models import User
from .models import (
    RideAdvert,
    Ride,
    Vehicle,
    Schedule,
    Route,
)


class RideTests(TestCase):

    fixtures = ['users.json', 'advert.json', ]

    def setUp(self):
        self.user1 = User.objects.all()[1]
        self.user2 = User.objects.all()[2]
        self.user3 = User.objects.all()[2]
        route1 = Route(
            start_latitude=43.1443, start_longitude=29.027217, start_radius=10.0,
            end_latitude=49.14, end_longitude=28.027217, end_radius=10.0
        )
        route1.save()
        # 1st
        self.advert1 = self._create_advert(
            self.user1,
            route1,
            Schedule(date="2014-01-11T13:12:32+02:00", is_recurring=False)
        )
        # 3
        self.advert2 = self._create_advert(
            self.user1,
            Route(
                start_latitude=41.00655, start_longitude=28.961083, start_radius=10.0,
                end_latitude=41.082255, end_longitude=29.06561, end_radius=10.0),
            Schedule(date="2014-01-13T13:17:52+02:00", is_recurring=False)
        )
        # 2
        self.advert3 = self._create_advert(
            self.user3,
            Route(
                start_latitude=41.00655, start_longitude=28.961083, start_radius=10.0,
                end_latitude=41.082255, end_longitude=29.06561, end_radius=10.0),
            Schedule(date="2014-01-13T13:16:02+02:00", is_recurring=False)
        )
        # recurring rides
        # 4
        self.advert4 = self._create_advert(
            self.user3,
            Route(
                start_latitude=41.00655, start_longitude=28.961083, start_radius=10.0,
                end_latitude=41.082255, end_longitude=29.06561, end_radius=10.0),
            Schedule(date="2014-02-23T13:17:52+02:00",
                     is_recurring=True, byweekday="1,2,3,4,5,6,7")
        )
        # 5
        self.advert5 = self._create_advert(
            self.user1,
            Route(
                start_latitude=41.00655, start_longitude=28.961083, start_radius=10.0,
                end_latitude=41.082255, end_longitude=29.06561, end_radius=10.0),
            Schedule(date="2014-03-13T13:17:52+02:00",
                     is_recurring=True, byweekday="1,2,3,4,5,6,7")
        )
        # distant future advert
        self.advert6 = self._create_advert(
            self.user1,
            Route(
                start_latitude=41.00655, start_longitude=28.961083, start_radius=10.0,
                end_latitude=41.082255, end_longitude=29.06561, end_radius=10.0),
            Schedule(date="2014-11-13T13:16:02+02:00", is_recurring=False)
        )

    def _create_advert(self, driver, route, schedule):
        vehicle = Vehicle(brand="Mercedes", model="Nuri gibi", year=1989)
        vehicle.save()
        route.save()
        schedule.save()
        ad = RideAdvert(
            route=route,
            driver=driver,
            vehicle=vehicle,
            offerred_seats=3,
            price=50,
            schedule=schedule
        )
        ad.save()
        return ad

    def test_creating_ride_from_advert(self):
        """a ride can only be created from the deep copy of an advert"""
        advert = RideAdvert.objects.all()[0]
        ride = Ride.objects.create_from_advert(advert, [self.user3, ])

        self.assertNotEquals(
            ride.route.id, advert.route.id, "Route should've copied")
        self.assertNotEquals(
            ride.vehicle.id, advert.vehicle.id, "Route should've copied")
        self.assertEquals(
            ride.driver.id, advert.driver.id, "Drivers should be the same")
        self.assertEquals(ride.offerred_seats, advert.offerred_seats,
                          "Offered seats should be copied")
        self.assertEquals(ride.price, advert.price, "price should be copied")
        self.assertEquals(
            ride.currency, advert.currency, "currency should be copied")

        # this is a non recurring ride. dates most be the same
        self.assertEquals(ride.date, advert.schedule.date, "This is a non-recurring ride, dates must be the same")

        # let's make sure that user related fields work
        self.assertEqual(1, len(ride.passengers.all()))
        self.assertEqual(self.user3.username, ride.passengers.all()[0].username)
        self.assertEqual(self.user3.passenger_rides.all()[0].id, ride.id)
        self.assertEqual(0, len(self.user3.ride_set.all()))

    def test_creating_ride_from_recurring_advert(self):
        """on recurring adverts, ride can only be craeted on any of the event dates"""
        pass

    def test_getting_rides_and_adverts(self):
        """
        Ride search can get either `Ride` objects or `RideAdvert` objects
        If `Ride` object is found, it will be returned, else `RideAdvert`
        """
        Ride.objects.create_from_advert(self.advert2, [self.user3, self.user2, ])
        Ride.objects.create_from_advert(self.advert3, [self.user2, ])

        date = "2014-01-13T12:20:52+02:00"
        rides = RideAdvert.objects.rides(date)
        self.assertEqual(
            4, len(rides), "first one is expired")

        # test ride types
        self.assertEqual(rides[0].__class__.__name__, "Ride")
        self.assertEqual(rides[1].__class__.__name__, "Ride")
        self.assertEqual(rides[2].__class__.__name__, "RideAdvert")
        self.assertEqual(rides[3].__class__.__name__, "RideAdvert")

        # test sorting by ride date
        self.assertEqual(self.advert3.pk, rides[0].advert.pk)
        self.assertEqual(self.advert2.pk, rides[1].advert.pk)
        self.assertEqual(self.advert4.pk, rides[2].pk)
        self.assertEqual(self.advert5.pk, rides[3].pk)

    def test_getting_rides_by_date(self):
        date = "2014-01-13T12:20:52+02:00"
        rides = RideAdvert.objects.rides(date)
        self.assertEqual(
            4, len(rides), "first one is expired")

        # test sorting by ride date
        self.assertEqual(self.advert3.pk, rides[0].pk)
        self.assertEqual(self.advert2.pk, rides[1].pk)
        self.assertEqual(self.advert4.pk, rides[2].pk)
        self.assertEqual(self.advert5.pk, rides[3].pk)

        date = "2014-06-23T15:20:52+02:00"
        rides = RideAdvert.objects.rides(date)
        self.assertEqual(0, len(rides), "rides should've xpired")

        date = "2014-03-03T15:20:52+02:00"
        rides = RideAdvert.objects.rides(date)
        self.assertEqual(1, len(rides), "rides should've xpired")

    def test_getting_rides_by_route(self):
        """
        Rides must be found within coordinates' radius
        """

    def test_getting_rides_by_date_and_route(self):
        """docstring for test_getting_rides_by_date_and_route"""
        pass


class CarpoolUserTest(TestCase):

    def test_public_name(self):
        user = User.objects.create_user('aykut', 'aykut@veli.com', 'pass')
        user.first_name = "Aykut"
        user.last_name = "Kocaman"

        self.assertEqual("Aykut K.", user.public_name)

        user = User.objects.create_user('fterim', 'fatih@veli.com', 'pass')
        user.first_name = "Fatih"
        user.last_name = "Terim"

        self.assertEqual("Fatih T.", user.public_name)

        # no last name
        user = User.objects.create_user('hsukur', 'hakan@veli.com', 'pass')
        user.first_name = "Hakan"
        user.last_name = ""

        self.assertEqual("Hakan", user.public_name)

        # no first name
        user = User.objects.create_user('aturanw', 'arda@veli.com', 'pass')
        user.first_name = ""
        user.last_name = "Turan"

        self.assertEqual("Turan", user.public_name)

        # no first or last name
        user = User.objects.create_user('sabri', 'sabri@veli.com', 'pass')
        user.first_name = ""
        user.last_name = ""

        self.assertEqual("sabri", user.public_name)
