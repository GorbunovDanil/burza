"""
api.views
~~~~~~~~~
Burza REST endpoints:

POST /api/start/        → manual trigger of the price-filter pipeline
POST /api/rating/       → receive News-module ratings, forward sale list
GET  /api/favorites/    → return current favourites list
PUT  /api/favorites/    → replace favourites list with payload
GET  /api/logs/stream/  → Server-Sent-Events live log stream
"""
from __future__ import annotations

import asyncio
import logging
import pathlib
import time
from typing import Iterable

import httpx
from django.conf import settings
from django.http import StreamingHttpResponse
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from .files import load_favorites, save_favorites
from .pipeline import run as run_pipeline
from .serializers import RecordSerializer

log = logging.getLogger("burza")


# ---------------------------------------------------------------------------#
# 1. MANUAL PIPELINE TRIGGER                                                 #
# ---------------------------------------------------------------------------#
class StartViewSet(ViewSet):
    """
    POST /api/start/
    Body: {}
    """ 

    http_method_names = ["post"]

    def create(self, request, *args, **kwargs):
        run_pipeline()
        return Response({"ok": True})


# ---------------------------------------------------------------------------#
# 2. RECEIVE RATINGS FROM NEWS MODULE                                        #
# ---------------------------------------------------------------------------#
class RatingViewSet(ViewSet):
    """
    POST /api/rating/
    Body: [
      {"name": "MSFT", "date": 1708300800, "rating": 7, "sale": 0},
      ...
    ]
    """

    http_method_names = ["post"]

    def create(self, request, *args, **kwargs):
        serializer = RecordSerializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=False)  # ignore bad rows
        valid_rows = serializer.validated_data
        ignored = len(request.data) - len(valid_rows)

        if not valid_rows:
            return Response(
                {"accepted": 0, "ignored": ignored},
                status=status.HTTP_200_OK,
            )

        threshold = settings.RATING_LIMIT
        sale_payload = [
            {**row, "sale": 1}
            for row in valid_rows
            if row["rating"] >= threshold
        ]

        if sale_payload:
            with httpx.Client(
                verify="certs/partner_ca.pem", timeout=10
            ) as client:
                resp = client.post(
                    "https://partner-url:8000/salestock", json=sale_payload
                )
                log.info(
                    "Forwarded %s sale items → partner %s",
                    len(sale_payload),
                    resp.status_code,
                )

        return Response(
            {
                "accepted": len(valid_rows),
                "ignored": ignored,
            },
            status=status.HTTP_200_OK,
        )


# ---------------------------------------------------------------------------#
# 3. CRUD FOR FAVOURITES (FILE STORAGE)                                      #
# ---------------------------------------------------------------------------#
class FavouritesSerializer(serializers.Serializer):
    """Validates a plain list of tickers/strings."""

    tickers = serializers.ListField(
        child=serializers.CharField(max_length=16),
        allow_empty=False,
    )

    def to_representation(self, instance):
        # DRF expects dict→serialize; we just return raw list.
        return instance


class FavouritesViewSet(ViewSet):
    """
    GET /api/favorites/   → ["MSFT", "AAPL"]
    PUT /api/favorites/   → replaces list
      Body: { "tickers": ["MSFT", "AAPL"] }
    """

    http_method_names = ["get", "put"]

    def list(self, request, *args, **kwargs):  # GET
        return Response(load_favorites())

    def update(self, request, *args, **kwargs):  # PUT
        ser = FavouritesSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        save_favorites(ser.validated_data["tickers"])
        return Response(load_favorites())


# ---------------------------------------------------------------------------#
# 4. LIVE LOG STREAM (SERVER-SENT EVENTS)                                    #
# ---------------------------------------------------------------------------#
LOG_FILE = pathlib.Path(__file__).resolve().parent.parent / "logs" / "burza.log"


def _tail_lines() -> Iterable[str]:
    """Generator that yields new lines appended to the log file."""
    LOG_FILE.parent.mkdir(exist_ok=True)
    LOG_FILE.touch(exist_ok=True)
    with LOG_FILE.open() as f:
        f.seek(0, 2)  # move to EOF
        while True:
            line = f.readline()
            if line:
                yield f"data: {line.rstrip()}\n\n"
            else:
                time.sleep(0.4)


def log_stream(request):
    """
    GET /api/logs/stream/
    Returns text/event-stream with log lines.
    """
    response = StreamingHttpResponse(
        _tail_lines(), content_type="text/event-stream"
    )
    response["Cache-Control"] = "no-cache"
    return response
