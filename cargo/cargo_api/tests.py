from django.urls import reverse
from rest_framework.test import APITestCase

from cargo_api.models import Location, Cargo, Transport


class Base(APITestCase):
    def setUp(self) -> None:
        self.loc_from = Location.objects.create(
            city="Adjuntas",
            state="Puerto Rico",
            mail_index="1234A",
            latitude=18.18027,
            longitude=-66.75266,
        )
        self.loc_to = Location.objects.create(
            city="Aguada",
            state="Puerto Rico",
            mail_index="4321B",
            latitude=18.36075,
            longitude=-67.17541,
        )
        self.cargo = Cargo.objects.create(
            pick_up=self.loc_from,
            delivery=self.loc_to,
        )


class ModelLocation(Base):
    def test_get_distance(self):
        result = Location.get_distance(
            query_from=self.loc_from,
            query_to=self.loc_to,
        )
        self.assertEquals(result, 30.42412261683947)

    def test_get_location(self):
        data = Location.get_location(
            latitude=18.18027,
            longitude=-66.75266,
        )
        data2 = Location.get_location(
            latitude=18.36075,
            longitude=-67.17541,
        )
        self.assertEquals(data.city, "Adjuntas")
        self.assertEquals(data2.city, "Aguada")


class ModelCargo(Base):
    def test_get_cargo(self):
        data = Cargo.objects.get(id=1)
        self.assertEquals(data.id, 1)

    def test_add_cargo(self):
        result = Cargo.add_cargo(
            x_from=18.36075,
            x_to=-67.17541,
            y_from=18.18027,
            y_to=-66.75266,
        )
        data = Cargo.get_cargo(result.id)
        self.assertEquals(data.id, 2)

    def test_delete_cargo(self):
        result = Cargo.delete_cargo(1)
        cargo = Cargo.get_cargo(1)
        self.assertEquals(result, True)
        self.assertFalse(cargo)


class ModelTransport(Base):
    def setUp(self) -> None:
        super().setUp()
        self.vehicle = Transport.objects.create(
            unique_id="6543Q",
            location=self.loc_to,
            carrying_capacity=50,
        )
        self.vehicle2 = Transport.objects.create(
            unique_id="6223T",
            location=self.loc_from,
            carrying_capacity=50,
        )

    def test_get_transport_id(self):
        result = Transport.get_transport_id(1)
        self.assertEquals(result.unique_id, "6543Q")

    def test_check_distance(self):
        result1 = Location.get_distance(
            query_from=self.vehicle.location, query_to=self.loc_from
        )
        result2 = Location.get_distance(
            query_from=self.vehicle2.location, query_to=self.loc_from
        )

        self.assertEquals(round(result1), 30)
        self.assertEquals(result2, 0)

    def test_get_in_range(self):
        data = Transport.get_in_range(cargo_id=1)
        cargo = Cargo.get_cargo(id=1)

        result = [
            {
                "unique_id": x.unique_id,
                "distance": round(
                    Location.get_distance(
                        query_from=cargo.pick_up,
                        query_to=x.location,
                    )
                ),
            }
            for x in data
        ]
        answer = [
            {"unique_id": "6543Q", "distance": 30},
            {"unique_id": "6223T", "distance": 0},
        ]
        self.assertEquals(result, answer)


class CargoAPI(Base):
    def setUp(self) -> None:
        super().setUp()
        self.vehicle = Transport.objects.create(
            unique_id="6543Q",
            location=self.loc_to,
            carrying_capacity=50,
        )

    def test_get(self):
        url = reverse("api:cargo")
        response = self.client.get(url)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(
            response.data,
            {
                'message': [{
                    "id": 1,
                    "pick-up": "Adjuntas",
                    "delivery-up": "Aguada",
                    "vehicle_around": [{"distance": 30, "unique_id": "6543Q"}],
                }],
            }
        )

    def test_post_success(self):
        url = reverse("api:cargo")
        response = self.client.post(
            url,
            data={
                "pick_up_latitude": 18.36075,
                "pick_up_longitude": -67.17541,
                "delivery_latitude": 18.18027,
                "delivery_longitude": -66.75266,
            },
        )

        self.assertEquals(response.status_code, 201)
        self.assertEquals(response.data, {"message": f"New cargo was created"})


class CargoDetailAPI(Base):
    def setUp(self) -> None:
        super().setUp()
        self.vehicle = Transport.objects.create(
            unique_id="6543Q",
            location=self.loc_to,
            carrying_capacity=50,
        )
        self.vehicle2 = Transport.objects.create(
            unique_id="6223T",
            location=self.loc_from,
            carrying_capacity=50,
        )

    def test_get(self):
        url = reverse("api:cargo_detail", kwargs={"id": 1})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        answer = {
            "pick_up": "Adjuntas",
            "delivery": "Aguada",
            "weight": 1,
            "description": None,
            "vehicle": [
                {"distance": 30, "unique_id": "6543Q"},
                {"distance": 0, "unique_id": "6223T"},
            ],
        }
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.data, answer)

    def test_put(self):
        url = reverse("api:cargo_detail", kwargs={"id": 1})
        response = self.client.put(
            url,
            data={
                "description": "Test",
                "weight": 100,
            },
        )
        cargo = Cargo.get_cargo(1)
        self.assertEquals(cargo.weight, 100)
        self.assertEquals(cargo.description, "Test")
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.data, {"message": "Updated"})

    def test_delete(self):
        url = reverse("api:cargo_detail", kwargs={"id": 1})
        response = self.client.delete(url)
        self.assertEquals(response.status_code, 204)
