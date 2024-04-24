from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User
from .admin_controller import AdminEmailController

@receiver(post_save, sender=User)
def send_admin_creation_notification(sender, instance, created, **kwargs):
    if created and instance.role == 'admin':
        AdminEmailController.send_admin_account_notification(instance)
