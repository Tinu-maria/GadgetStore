from django.db.models import signals
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings


@receiver(signals.post_save, sender=User)
def create_user(sender, instance, created, **kwargs):
    if created:
        send_mail(
            "Welcome to our store",
            "Thank you for joining our store! We hope you enjoy our store.",
            settings.EMAIL_HOST_USER,
            [instance.email],
            fail_silently=True,
        )