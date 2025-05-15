from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action


class StartViewSet(ViewSet):
    def create(self, request):
        # This will run when you POST to /api/start/
        print("StartViewSet triggered!")
        return Response({"status": "Started successfully"})


class RatingViewSet(ViewSet):
    def create(self, request):
        # This will run when you POST to /api/rating/
        print("RatingViewSet triggered!")
        return Response({"status": "Ratings received"})
