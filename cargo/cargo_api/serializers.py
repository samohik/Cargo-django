from rest_framework import serializers

from .models import Cargo


class CargoSerializer(serializers.ModelSerializer):
    pick_up_latitude = serializers.FloatField()
    pick_up_longitude = serializers.FloatField()
    delivery_latitude = serializers.FloatField()
    delivery_longitude = serializers.FloatField()

    class Meta:
        model = Cargo
        fields = [
            "pick_up_latitude",
            "pick_up_longitude",
            "delivery_latitude",
            "delivery_longitude",
        ]


class CargoDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cargo
        fields = ["weight", "description"]

    def update(self, instance, validated_data):
        instance.weight = validated_data.get("weight", instance.weight)
        instance.description = validated_data.get("description", instance.description)
        instance.save()
        return instance
