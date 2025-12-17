"""
Model representing a doctor profile within the telemedicine system.
This model stores professional  details linked to a user account.
"""
from django.db import models
from django.conf import settings
import uuid

class Doctor(models.Model):
    """
    Represents a doctor registered in the system.
    Each doctor is linked to exactly one user account.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE )
    date_of_birth = models.DateField()
    mobile_number = models.CharField(max_length=20, unique=True)
    address = models.TextField(blank=True)

    specialization = models.CharField(max_length=255)
    license_number = models.CharField(max_length=50, unique=True)

    # Doctor must be approved by admin before working
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"Dr. {self.user.first_name} {self.user.last_name} -{self.specialization}"



