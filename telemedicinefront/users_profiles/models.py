from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class UserProfile(models.Model):
    ROLE_CHOICES = [
        ("patient", "Patient"),
        ("doctor", "Doctor"),
    ]

    VERIFICATION_STATUS = [
        ("pending", "Pending Review"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ]

    # Links the Django User (authentication)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Role of person: doctor or patient
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    # All login users must have these)
    phone = models.CharField(max_length=16, unique=True)
    id_number = models.CharField(max_length=16, unique=True)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=8)

    # Doctor-specific fields (optional for patients)
    specialty = models.CharField(max_length=50, null=True, blank=True)
    license_number = models.CharField(max_length=50, null=True, blank=True)

    # verification status
    verification_status = models.CharField(
        max_length=20,
        choices=VERIFICATION_STATUS,
        default="pending"
    )

    created_at = models.DateTimeField(auto_now_add=True)



    def __str__(self):
        return f"{self.user.username} ({self.role})"
