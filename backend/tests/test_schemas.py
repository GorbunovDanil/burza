# backend/tests/test_schemas.py

import pytest
from pydantic import ValidationError
from api.schemas import Record    # or change to your actual class name

def test_valid_record():
    r = Record(name="MSFT", date=1_700_000_000, rating=0, sale=1)
    assert r.name == "MSFT"

@pytest.mark.parametrize("bad", [
    {"name": "X", "date": -1, "rating": 0,  "sale": 0},
    {"name": "Y", "date": 1,  "rating": 20, "sale": 0},
    {"name": "Y", "date": 1,  "rating": 0,  "sale": 2},
])
def test_invalid_schema(bad):
    with pytest.raises(ValidationError):
        Record(**bad)
