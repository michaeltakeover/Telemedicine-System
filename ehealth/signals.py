from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import NewUser, Patient, Doctor



@receiver(post_save, sender=NewUser)
def create_user_profile(sender, instance, created, **kwargs):
    if not created:
        return

    if instance.role == "patient":
        Patient.objects.get_or_create(
            user=instance,
            defaults={
                "date_of_birth": "2000-01-01",
                "mobile_number": f"PAT-{instance.id}",
                "address": "",
                "preferred_payment_mode": "insurance",
            },
        )

    elif instance.role == "doctor":
        Doctor.objects.get_or_create(
            user=instance,
            defaults={
                "date_of_birth": "1980-01-01",
                "mobile_number": f"DOC-{instance.id}",
                "address": "",
                "specialization": "General",
                "license_number": f"LIC-{instance.id}",
                "is_approved": False,
            },
        )
