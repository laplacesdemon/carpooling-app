import copy
from itertools import chain
from operator import attrgetter
from dateutil.relativedelta import relativedelta
from dateutil import parser
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from model_utils.models import TimeStampedModel
from model_utils import Choices


@property
def public_name(self):
    """represents the name in following format: Ali K."""
    if self.first_name and self.last_name:
        return "%s %s." % (self.first_name, self.last_name[0])

    if self.first_name and not self.last_name:
        return self.first_name

    if self.last_name and not self.first_name:
        return self.last_name

    if not self.first_name and not self.last_name:
        return self.username


User.add_to_class('public_name', public_name)


class Route(models.Model):
    """
    The route defines the start and arrival destinations in coordinates
    """
    start_latitude = models.FloatField(_("Start Latitude"), help_text=_("Start location's latitude (departure) in decimal degrees (ex: 40.990033)."))
    start_longitude = models.FloatField(_("Start Longitude"), help_text=_("Start location's longitude (departure) in decimal degrees (ex: 29.0424)."))
    start_radius = models.FloatField(_("Start Radius"), default=4, help_text=_("The radius of the circle around departure point"))
    start_address = models.CharField(_("Start Address"), max_length=255, blank=True, help_text=_("Human readable address for start location"))
    end_latitude = models.FloatField(_("End Latitude"), help_text=_("End location's latitude (arrival) in decimal degrees (ex: 40.990033)."))
    end_longitude = models.FloatField(_("End Longitude"), help_text=_("End location's longitude (arrival) in decimal degrees (ex: 29.0424)."))
    end_radius = models.FloatField(_("End Radius"), default=4, help_text=_("The radius of the circle around arrival point (in km)"))
    end_address = models.CharField(_("End Address"), max_length=255, blank=True, help_text=_("Human readable address for destination location"))

    def __unicode__(self):
        """string representation"""
        return "%s -> %s" % (self.start_address, self.end_address)


DAYS = (
    (1, _("Monday")),
    (2, _("Tuesday")),
    (3, _("Wednesday")),
    (4, _("Thursday")),
    (5, _("Friday")),
    (6, _("Saturday")),
    (7, _("Sunday")),
)


class Schedule(models.Model):
    """
    Schedule determines the date(s) for the rides.
    It can be recurring dates or a one-time date.
    Recurring dates are daily and recurs at the same time
    that the `date` attribute is by the weekday.
    `byweekday` attribute determines the days of the weeks
    by enumerating them. 1 is for monday, 2 is for tuesday, etc.
    """

    date = models.DateTimeField(_("Date and Time"),
                                help_text=_("The ride date. If one-time event, the ride happens at this date and time. "
                                            "If recurring, ride takes places at the same time of each weekday determined by `byweekday`"))
    is_recurring = models.BooleanField(_("Is Recurring?"), default=0, help_text=_("Determines if it is a recurring ride."))
    byweekday = models.CommaSeparatedIntegerField(_("By Weekday"), max_length=16, blank=True, null=True,
                                                  help_text=_("Determines the daily recurrance of the ride. The ride recurs each day of this attribute."
                                                              "Dates are 1 for monday, 2 for tuesday, etc"))

    def __unicode__(self):
        """string representation of the object"""
        if self.is_recurring:
            return "Her %s, %s" % (self.byweekday, self.date.strftime("%Y-%m-%d %H:%M:%S"))
        else:
            return "Tek sefer: %s" % self.date.strftime("%Y-%m-%d %H:%M:%S")


class Vehicle(models.Model):
    """
    The vehicle represents the ride car.
    """
    brand = models.CharField(_("Brand"), max_length=64)
    model = models.CharField(_("Model"), max_length=64, blank=True)
    year = models.PositiveSmallIntegerField(_("Year"), max_length=4, blank=True, help_text=_("Year that the vehicle is manufactured"))
    seat_capacity = models.PositiveSmallIntegerField(_("Seats Capacity"), default=3, help_text=_("How many seats that this vehicle has?"))

    def __unicode__(self):
        """string representation"""
        return "%s model %s %s" % (self.year, self.brand, self.model)


class BaseRide(TimeStampedModel):
    """
    Abstract ride model that both `Ride` and `RideAdvert` inherits from.
    """

    class Meta:
        abstract = True

    route = models.OneToOneField("Route")
    driver = models.ForeignKey(User)
    vehicle = models.ForeignKey("Vehicle")
    offerred_seats = models.PositiveSmallIntegerField(_("Offerred Seats"), default=3, help_text=_("Determines the seats that are available for the ride"
                                                                                                  "Different that the vehicle's seats."))
    price = models.PositiveSmallIntegerField(_("Price"), help_text=_("The offerred price for the ride"))
    currency = models.CharField(_("Currency"), max_length=10, default="TRY")

    @property
    def is_advert(self):
        """Returns True if this is a `RideAdvert` instance"""
        return True

    @property
    def registered_seats(self):
        """Returns number of seats taken / total seats."""
        return "0/%d" % self.offerred_seats


class RideAdvertManager(models.Manager):

    def rides(self, a_date=None, a_route=None):
        """
        Searches for rides by date and/or route.
        Ride search can get either `Ride` objects or `RideAdvert` objects
        If `Ride` object is found, it will be returned, else `RideAdvert`

        results will start from the given date to the next 3months
        """
        if a_date:
            date_plus_3_months = parser.parse(a_date) + relativedelta(months=+3)

        # fetch rides
        q1 = Ride.objects
        if a_date:
            q1 = q1.filter(date__gte=a_date).filter(date__lte=date_plus_3_months)
        if a_route:
            pass
        rides = q1.all()

        # get ids of rides
        advert_ids = list()
        for ride in rides:
            advert_ids.append(ride.advert.pk)

        # fetch ride adverts
        q = RideAdvert.objects
        if a_date:
            q = q.filter(schedule__date__gte=a_date).filter(schedule__date__lte=date_plus_3_months)
        if a_route:
            pass
        q = q.exclude(pk__in=advert_ids)
        adverts = q.all()

        # merge results
        # sort results by the advert date
        res = sorted(
            chain(rides, adverts),
            key=attrgetter('date')
        )

        return res


class RideAdvert(BaseRide):
    """
    Ride advert represents rides to be displayed in search results.
    This is not an actual ride object (see `Ride`).
    """
    schedule = models.OneToOneField("Schedule")

    objects = RideAdvertManager()

    def __unicode__(self):
        """string representation of the class"""
        return "Planned Ride #%d by %s - %s" % (self.pk, self.driver.username, self.schedule.date.strftime("%Y-%m-%d %H:%M:%S"))

    @property
    def date(self):
        """returns the first available date of the advert schedule"""
        # TODO recurring dates
        return self.schedule.date


class RideManager(models.Manager):

    def create_from_advert(self, advert, passengers, date=None):
        """
        Creates a ride instance from the advert data.
        The advert data on shared attributes must be copied.

        `date` param is required for recurring rides.
        """
        ride = Ride()

        # copy route
        route = copy.deepcopy(advert.route)
        route.pk = None
        route.save()
        ride.route = route

        # copy vehicle
        # TODO copy vehicle pictures
        vehicle = copy.deepcopy(advert.vehicle)
        vehicle.pk = None
        vehicle.save()
        ride.vehicle = vehicle

        ride.driver = advert.driver
        ride.offerred_seats = advert.offerred_seats
        ride.price = advert.price
        ride.currency = advert.currency
        ride.advert = advert

        # ride date: if schedule is recurring
        if advert.schedule.is_recurring:
            ride.date = date
        else:
            ride.date = advert.schedule.date

        ride.save()

        # add passengers
        for passenger in passengers:
            ride.passengers.add(passenger)

        return ride


class Ride(BaseRide):
    """
    A ride represents an actual ride that at least one passenger is subscribed.
    In search results, `Ride` objects are displayed available. Otherwise `RideAdvert` objects are displayed.
    """
    STATES = Choices(
        (1, "PENDING", "Pending"),
        (2, "SUCCESS", "Successfully Completed"),
        (3, "FAILED", "Failed"),
        (4, "FINALIZED_WITH_PROBLEMS", "Finalized with problems"),
    )

    advert = models.OneToOneField("RideAdvert")
    date = models.DateTimeField(_("Date and Time"), help_text=_("Start Date and time of the ride"))
    state = models.PositiveSmallIntegerField(_("State"), choices=STATES, default=STATES.PENDING)
    passengers = models.ManyToManyField(User, related_name="passenger_rides")

    objects = RideManager()

    def __unicode__(self):
        """string representation"""
        return "Ride #%d by %s - %s" % (self.pk, self.driver.username, self.date.strftime("%Y-%m-%d %H:%M:%S"))

    @property
    def is_advert(self):
        """Returns True if this is a `RideAdvert` instance"""
        return False

    @property
    def registered_seats(self):
        """Returns number of seats. If Advert it returns `offerred_seats`."""
        return "%d/%d" % (self.passengers.count(), self.offerred_seats)


class RideRequest(TimeStampedModel):
    """
    RideRequest determines the requests that are done by passenger for a particular ride
    """
    OPTIONS = Choices(
        (1, "PENDING", _("Pending")),
        (2, "REJECTED", _("Rejected")),
        (3, "ACCEPTED", _("Accepted")),
    )

    ride = models.ForeignKey("Ride", related_name="requests")
    passenger = models.ForeignKey(User)
    status = models.PositiveSmallIntegerField(_("Status"), choices=OPTIONS, default=OPTIONS.PENDING)
    passenger_notes = models.TextField(_("Passenger Notes"), blank=True)
    driver_notes = models.TextField(_("Driver Notes"), blank=True)

    def __unicode__(self):
        """string representation"""
        return "By %s for ride #%d - %s" % (self.passenger.username, self.ride.id, self.status)


class RideExperience(TimeStampedModel):
    """
    RideExperience represents the user's (driver or passenger) experience with a ride
    """
    STATES = Choices(
        (1, "NO_DRIVER", _("No Driver")),  # by passenger
        (2, "CANCELLED", _("Cancelled")),  # by the driver
        (3, "POSITIVE", _("Positive")),
        (4, "NEGATIVE", _("Negative")),
    )
    ride = models.ForeignKey("Ride", related_name="experiences")
    user = models.ForeignKey(User)
    state = models.PositiveSmallIntegerField(_("State"), choices=STATES)
    note = models.TextField(_("Note"), blank=True)

    def __unicode__(self):
        """string representation"""
        return "By %s for rider #%d - %s" % (self.user.username, self.ride.id, self.state)
