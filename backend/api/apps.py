# backend/api/apps.py
from django.apps import AppConfig

class ApiConfig(AppConfig):
    name = "api"

    def ready(self):
        from . import scheduler
        scheduler.start()
