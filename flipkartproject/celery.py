import os
from celery import Celery
from celery.schedules import crontab
import flipkart_app.tasks

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "flipkartproject.settings")
# we use .setdefault() of os.environ to assure that Django project’s settings.py module is accessible through
# "DJANGO_SETTINGS_MODULE" key

app = Celery("flipkartproject")
# we create the Celery application instance and provide the name of the main module as an argument

# app.conf.enable_utc = False
# app.conf.update(timezone='Asia/Kolkata')

app.config_from_object("django.conf:settings", namespace="CELERY")
# we define the Django settings file as the configuration file for Celery and provide a namespace, "CELERY"

# Celery beat settings
# app.conf.beat_schedule = {
#     'send_mail_everyday': {
#         'task': 'flipkart_app.tasks.send_enquiry_email_task',
#         'schedule': crontab(hour=14, minute=51),
#     }
# }

# app.autodiscover_tasks()
# we tell our Celery application instance to automatically find all tasks in each app of our Django project


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')  # prints all metadata about the request when task is received
