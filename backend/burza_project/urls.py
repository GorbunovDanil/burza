# backend/burza_project/urls.py

from django.urls import include, path
from rest_framework.routers import DefaultRouter
from api.views import StartViewSet, RatingViewSet, FavouritesViewSet, log_stream

router = DefaultRouter()
router.register(r"start",  StartViewSet,   basename="start")
router.register(r"rating", RatingViewSet,  basename="rating")

urlpatterns = [
    path("api/", include(router.urls)),
    # Manual GET/PUT on /api/favorites/
    path(
        "api/favorites/",
        FavouritesViewSet.as_view({"get": "list", "put": "update"}),
        name="favorites",
    ),
    path("api/logs/stream/", log_stream),
]
