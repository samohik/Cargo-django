from django.contrib import admin

from .models import Location, Cargo, Transport


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = [
        "city",
        "state",
        "mail_index",
        "latitude",
        "longitude",
    ]


@admin.register(Cargo)
class CargoAdmin(admin.ModelAdmin):
    list_display = [
        "delivery",
        "weight",
        "description",
    ]


@admin.register(Transport)
class TransportAdmin(admin.ModelAdmin):
    list_display = [
        "unique_id",
        "location",
        "carrying_capacity",
    ]
