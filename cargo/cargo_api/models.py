from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.db import models
from django.db.models import Q
from geopy import distance


class Location(models.Model):
    city = models.CharField(
        verbose_name="City",
        max_length=120,
    )
    state = models.CharField(
        verbose_name="State",
        max_length=120,
    )
    mail_index = models.CharField(
        verbose_name="Mail index",
        max_length=120,
    )
    latitude = models.FloatField(
        verbose_name="Latitude",
    )
    longitude = models.FloatField(
        verbose_name="Longitude",
    )

    def __str__(self):
        return str(self.city)

    def dump_location_csv(self):
        pass

    @classmethod
    def get_location(cls, latitude, longitude):
        data = Location.objects.filter(
            latitude=latitude,
            longitude=longitude,
        )
        if data:
            return data.first()
        else:
            return False

    @classmethod
    def get_distance(cls, query_from, query_to) -> float:
        loc_1 = (query_to.latitude, query_to.longitude)
        loc_2 = (query_from.latitude, query_from.longitude)
        data = distance.distance(loc_1, loc_2).miles
        return data


class Cargo(models.Model):
    pick_up = models.ForeignKey(
        Location, related_name="cargo_pick_up", on_delete=models.CASCADE
    )
    delivery = models.ForeignKey(
        Location, related_name="cargo_delivery", on_delete=models.CASCADE
    )
    weight = models.PositiveIntegerField(
        verbose_name="Weight",
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(1000)],
    )
    description = models.TextField(verbose_name="Description", blank=True, null=True)

    def __str__(self):
        return str(self.id)

    @classmethod
    def get_cargo(cls, id):
        data = Cargo.objects.filter(id=id)
        if data:
            return data.get()
        else:
            return False

    @classmethod
    def add_cargo(cls, x_from, x_to, y_from, y_to):
        loc_x = Location.get_location(x_from, x_to)
        loc_y = Location.get_location(y_from, y_to)
        if loc_x and loc_y:
            cargo = Cargo.objects.create(
                pick_up=loc_x,
                delivery=loc_y,
            )
            return cargo
        return

    @classmethod
    def delete_cargo(cls, id):
        cargo = Cargo.get_cargo(id)
        if cargo:
            cargo.delete()
            return True
        else:
            return


class Transport(models.Model):
    unique_id = models.CharField(
        max_length=5,
        unique=True,
        validators=[
            RegexValidator(
                regex="\d{4}[A-Z]",
                message="Field must contain four integer and one upper alfabet.",
            )
        ],
    )
    location = models.ForeignKey(
        "Location",
        verbose_name="Transport location",
        on_delete=models.CASCADE,
    )
    carrying_capacity = models.PositiveIntegerField(
        verbose_name="Carrying capacity",
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(1000)],
    )

    def __str__(self):
        return str(self.id)

    @classmethod
    def get_transport(cls):
        return Transport.objects.all()

    @classmethod
    def get_transport_id(cls, id):
        data = Transport.objects.filter(id=id)
        if data:
            return data.first()
        else:
            return

    @classmethod
    def get_in_range(cls, cargo_id, miles: int = 450):
        data = Cargo.get_cargo(id=cargo_id)
        if data:
            lat = data.pick_up.latitude
            lon = data.pick_up.longitude

            nearby_transport = Transport.objects.filter(
                Q(location__latitude__range=(lat - (miles / 69), lat + (miles / 69))),
                Q(location__longitude__range=(lon - (miles / 69), lon + (miles / 69))),
            )
            return nearby_transport
