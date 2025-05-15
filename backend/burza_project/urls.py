# backend/burza_project/urls.py
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from api.views import StartViewSet, RatingViewSet, FavouritesViewSet, log_stream

router = DefaultRouter()
router.register(r"start", StartViewSet,     basename="start")
router.register(r"rating", RatingViewSet,   basename="rating")
router.register(r"favorites", FavouritesViewSet, basename="favorites")

urlpatterns = [
    path("api/", include(router.urls)),
    path("api/logs/stream/", log_stream),
]