# To make sure the Celery app is loaded when we start Django

from .celery import app as celery_app

__all__ = ("celery_app",)