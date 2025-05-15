from pydantic import BaseModel, conint

# ---------------------------------------------------------------------------
#  DRF serializers for runtime (unchanged)
# ---------------------------------------------------------------------------
from rest_framework import serializers
import time


class RecordSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=64)
    date = serializers.IntegerField()
    rating = serializers.IntegerField(min_value=-10, max_value=10)
    sale = serializers.IntegerField(min_value=0, max_value=1)

    def validate_date(self, value):
        if value > int(time.time()) + 60:
            raise serializers.ValidationError("date is in the future")
        return value


# ---------------------------------------------------------------------------
#  Pydantic Record model –- used only by unit-tests
# ---------------------------------------------------------------------------
class Record(BaseModel):
    """Lightweight schema imported by tests/test_schemas.py"""
    name: str
    date: conint(ge=0)                 # must be ≥ 0 (unix epoch)
    rating: conint(ge=-10, le=10)
    sale: conint(ge=0, le=1)
