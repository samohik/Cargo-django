from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Cargo, Transport, Location
from .serializers import CargoSerializer, CargoDetailSerializer


class CargoView(APIView):
    serializer_class = CargoSerializer
    queryset = Cargo.objects.select_related("pick_up", "delivery")

    def get(self, request) -> Response:
        """
        Getting a list of cargo.
        """
        data = self.queryset.all()
        list_data = []
        for item_cargo in data:
            vehicles = Transport.get_in_range(item_cargo.id)
            cargo = {
                "id": item_cargo.id,
                "pick-up": item_cargo.pick_up.city,
                "delivery-up": item_cargo.delivery.city,
                "vehicle_around": [
                    {
                        "distance": round(
                            Location.get_distance(
                                item_vehicle.location,
                                item_cargo.pick_up,
                            )
                        ),
                        "unique_id": item_vehicle.unique_id,
                    }
                    for item_vehicle in vehicles
                ],
            }
            list_data.append(cargo)
        return Response({"message": list_data}, status=status.HTTP_200_OK)

    def post(self, request) -> Response:
        """
        Creating a new cargo.
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            pick_up_latitude = serializer.validated_data["pick_up_latitude"]
            pick_up_longitude = serializer.validated_data["pick_up_longitude"]
            delivery_latitude = serializer.validated_data["delivery_latitude"]
            delivery_longitude = serializer.validated_data["delivery_longitude"]

            result = Cargo.add_cargo(
                x_from=pick_up_latitude,
                x_to=pick_up_longitude,
                y_from=delivery_latitude,
                y_to=delivery_longitude,
            )
            if result:
                return Response(
                    {"message": f"New cargo was created"},
                    status=status.HTTP_201_CREATED,
                )
        return Response(
            {"message": "Not valid data"}, status=status.HTTP_400_BAD_REQUEST
        )


class CargoDetailView(APIView):
    serializer_class = CargoDetailSerializer

    def get(self, request, id: int) -> Response:
        """
        Obtaining information about a specific cargo.
        """
        cargo = Cargo.get_cargo(id=id)
        if cargo:
            vehicles = Transport.get_transport()
            response = {
                "pick_up": cargo.pick_up.city,
                "delivery": cargo.delivery.city,
                "weight": cargo.weight,
                "description": cargo.description,
                "vehicle": [],
            }

            for item in vehicles:
                vehicle = {
                    "unique_id": item.unique_id,
                    "distance": round(
                        Location.get_distance(
                            query_from=cargo.pick_up, query_to=item.location
                        )
                    ),
                }
                response["vehicle"].append(vehicle)

            return Response(response, status=status.HTTP_200_OK)
        return Response({"message": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id: int) -> Response:
        """
        Editing cargo.
        """
        cargo = Cargo.get_cargo(id)
        if cargo:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.update(
                    instance=cargo, validated_data=serializer.validated_data
                )

                return Response({"message": "Updated"}, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"message": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST
                )
        return Response(
            {"message": "Cargo don exist"}, status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, id: int) -> Response:
        """
        Cargo removal.
        """
        result = Cargo.delete_cargo(id)
        if result:
            return Response({"message": "delete"}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"message": "Error"}, status=status.HTTP_400_BAD_REQUEST)
