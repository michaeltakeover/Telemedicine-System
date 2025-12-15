
from django.db import models
from django.conf import settings
from datetime import date
import uuid

class Patient(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField()
    mobile_number = models.CharField(max_length=20, unique= True)
    address = models.TextField(blank=True)

    PAYMENT_MODES = [
            ("insurance", "Insurance"),
            ("card", "Credit/Debit Card"),
            ("cash", "Cash"),
        ]
    preferred_payment_mode = models.CharField(max_length=50,choices=PAYMENT_MODES)

    def age(self):
        today = date.today()
        return (
            today.year
            - self.date_of_birth.year
            - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        )

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


#  CHILD PROFILE (Linked to Patient)


class ChildProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    parent = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="children")
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100)

    date_of_birth = models.DateField()

    def age(self):
        today = date.today()
        return (
            today.year
            - self.date_of_birth.year
            - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        )

    def __str__(self):
        return f"{self.first_name} {self.last_name} (Child)"


