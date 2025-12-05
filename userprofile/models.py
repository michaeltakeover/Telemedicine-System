from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone


# Create your models here.
class UserProfile(models.Model):

    #  Users can  be Doctor or Patient
    ROLES = [
        ("patient", "Patient"),
        ("doctor", "Doctor"),
    ]

    #  Doctor must be approved by admin
    VERIFICATION_STATUS = [
        ("pending", "Pending Review"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ]

    # 3. Gender options
    GENDER = [
        ("male", "Male"),
        ("female", "Female"),
        ("prefer not to say", "Prefer not to say"),
    ]

    # Connect UserProfile to Django User , roles can be Doctor or Patient
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLES)

    #Common fields for both doctors & patients
    mobile_number = models.CharField(max_length=16, unique=True)
    id_number = models.CharField(max_length=16, unique=True)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=18, choices=GENDER)

    # Doctor-specific fields
    specialization = models.CharField(max_length=50, null=True, blank=True)
    license_number = models.CharField(max_length=50, null=True, blank=True)
    verification_status = models.BooleanField(default=False)


    # Doctor verification process
    #verification_status = models.CharField(
     #   max_length=20,
      #  choices=VERIFICATION_STATUS,
       # default="pending"
    #)

    created_at = models.DateTimeField(auto_now_add=True)

    # Ensure date_of_birth is not in the future
    def check_date(self):
        if self.date_of_birth > timezone.now().date():
            raise ValidationError("Date of birth cannot be in the future.")

    def __str__(self):
        return f"{self.user.username} ({self.role})"
