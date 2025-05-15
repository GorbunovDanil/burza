# backend/tests/test_serializers.py

import pytest
from rest_framework.exceptions import ValidationError
from api.serializers import RecordSerializer
from api.views import FavouritesSerializer

def test_record_serializer_valid():
    data = {"name":"A", "date":1, "rating":5, "sale":0}
    ser = RecordSerializer(data=data)
    assert ser.is_valid()
    assert ser.validated_data["rating"] == 5

def test_record_serializer_invalid():
    data = {"name":"A"}
    ser = RecordSerializer(data=data)
    with pytest.raises(ValidationError):
        ser.is_valid(raise_exception=True)

def test_favourites_serializer_valid():
    ser = FavouritesSerializer(data={"tickers":["X","Y"]})
    assert ser.is_valid()

def test_favourites_serializer_invalid():
    ser = FavouritesSerializer(data={"tickers":[]})
    with pytest.raises(ValidationError):
        ser.is_valid(raise_exception=True)
