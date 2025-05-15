# backend/tests/test_logs.py

from django.test import RequestFactory
from api.logs import log_stream

def test_log_stream_view():
    """GET /api/logs/stream/ returns an SSE response."""
    rf = RequestFactory()
    response = log_stream(rf.get("/api/logs/stream/"))
    assert response.status_code == 200
    assert response["Content-Type"] == "text/event-stream"
