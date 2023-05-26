from django.urls import path

from .views import CargoView, CargoDetailView

app_name = "api"


urlpatterns = [
    path("cargo/", CargoView.as_view(), name="cargo"),
    path("cargo/<int:id>/", CargoDetailView.as_view(), name="cargo_detail"),
]
