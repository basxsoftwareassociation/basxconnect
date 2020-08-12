from celery import Celery

# DJANGO_SETTINGS_MODULE environment variable must be set before this module is imported

app = Celery("basxconnect")

# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
