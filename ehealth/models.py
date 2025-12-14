from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager
from django.contrib.auth import get_user_model
from datetime import date
from django.conf import settings
User = settings.AUTH_USER_MODEL
import uuid


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        return self.create_user(email, password, **extra_fields)

#  USER MODEL (LOGIN ACCOUNT)


class NewUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)


    ROLES = [
        ("patient", "Patient"),
        ("doctor", "Doctor"),
        ("admin", "Admin"),
    ]
    GENDER_CHOICES = [
        ("male", "Male"), ("female", "Female"), ("other", "Other"),]


    role = models.CharField(max_length=20, choices=ROLES, blank=False, null=False)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(max_length=10,choices=GENDER_CHOICES)

    # AbstractUser includes:
    # username, first_name, last_name, email, password, is_staff,
    # is_active, is_superuser, last_login, date_joined

    USERNAME_FIELD = "email"  # LOGIN with email
    REQUIRED_FIELDS = []  # No username required

    objects = UserManager()
    #User = get_user_model()

    def __str__(self):
        return f"{self.email} ({self.role})"

#  PATIENT PROFILE


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



#  DOCTOR PROFILE


class Doctor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField()
    mobile_number = models.CharField(max_length=20, unique=True)
    address = models.TextField(blank=True)

    specialization = models.CharField(max_length=255)
    license_number = models.CharField(max_length=50, unique=True)

    # Doctor must be approved by admin before working
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"Dr. {self.user.first_name} {self.user.last_name} ({self.specialization})"




#  APPOINTMENTS (Patient ↔ Doctor)


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

    blood_pressure = models.CharField(max_length=20)
    heart_rate = models.IntegerField()
    temperature = models.FloatField()
    oxygen_level = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    is_abnormal = models.BooleanField(default=False)


    def __str__(self):
        return f"Vitals for {self.patient.user.first_name} on {self.created_at.date()}"



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



#  CHAT MESSAGES (For chat consultations)


class ChatMessage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    consultation = models.ForeignKey(Consultation, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)  # doctor or patient
    message = models.TextField()

    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender.email} at  {self.timestamp}"



#  PRESCRIPTIONS


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



#  NOTIFICATIONS


class Notification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)

    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.first_name} {self.user.last_name} ({self.user.email})"

