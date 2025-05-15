from rest_framework.routers import DefaultRouter
from api.views import StartViewSet, RatingViewSet
from django.urls import include, path

router = DefaultRouter()
router.register(r"start", StartViewSet, basename="start")
router.register(r"rating", RatingViewSet, basename="rating")

urlpatterns = [
    path("api/", include(router.urls)),
]
