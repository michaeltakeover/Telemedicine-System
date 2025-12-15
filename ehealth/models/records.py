from django.db import models
from .patient import Patient, ChildProfile
from .doctor import Doctor
import uuid



class Appointment(models.Model):

    STATUS = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    child = models.ForeignKey(
        ChildProfile, blank=True, null=True,
        on_delete=models.SET_NULL,
        help_text="If appointment is for the child"
    )

    appointment_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS, default="pending")
    reason = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Appointment: {self.patient.user.first_name} with Dr. {self.doctor.user.last_name}"



#  VITAL SIGNS (Patient records their vitals, doctor can view)


class VitalSign(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="vitals")

    systolic_bp = models.IntegerField(null=True)
    diastolic_bp = models.IntegerField(null=True)
    heart_rate = models.IntegerField()
    temperature = models.FloatField()
    oxygen_level = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    is_abnormal = models.BooleanField(default=False)


    def __str__(self):
        return f"Vitals for {self.patient.user.first_name} on {self.created_at.date()}"

    def out_of_range_vitals(self):

        alerts = []

        if self.heart_rate < 60 or self.heart_rate > 100:
            alerts.append(f"Heart rate: {self.heart_rate} bpm")

        if self.systolic_bp < 90 or self.systolic_bp > 120:
            alerts.append(f"Blood Pressure: {self.systolic_bp} bpm")

        if self.oxygen_level < 60 or self.oxygen_level > 150:
            alerts.append(f"Oxygen Level: {self.oxygen_level}")

        if self.temperature < 36.1 or self.temperature > 37.8:
            alerts.append(f"Temperature: {self.temperature} °C")

        return alerts


#  CONSULTATION (Chat or Video)


class Consultation(models.Model):

    TYPE = [
        ("chat", "Chat"),
        ("video", "Video Call"),
    ]

    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE,related_name="consultation" )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)


    consultation_type = models.CharField(max_length=20, choices=TYPE)
    notes = models.TextField(blank=True)

    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.consultation_type} consultation for {self.appointment}"




class Prescription(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    consultation = models.ForeignKey(Consultation, on_delete=models.CASCADE,related_name="prescriptions")

    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)

    medication_name = models.CharField(max_length=255)
    dosage = models.CharField(max_length=100)
    instructions = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Prescription for {self.consultation.appointment.patient.user.first_name}"


