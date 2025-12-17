"""
Combined registration form for the Telemedicine System.

unified registration form that supports both Patient and Doctor account creation.
dynamically validates and persists role-specific data and uniqueness constraints.
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.utils.timezone import now
import uuid

from ..models import NewUser, Patient, Doctor

class CombinedRegistrationForm(UserCreationForm):
    ROLE_CHOICES = [
        ("patient", "Patient"),
        ("doctor", "Doctor"),
    ]
    role = forms.ChoiceField(choices=ROLE_CHOICES)
    username = None

    class Meta:
        model = NewUser
        fields = [
            "first_name",
            "middle_name",
            "last_name",
            "email",
            "gender",
            "role",
        ]

    # Patient fields
    patient_date_of_birth = forms.DateField(required=False, widget=forms.DateInput(attrs={"type": "date"}))
    patient_mobile_number = forms.CharField(required=False)
    patient_address = forms.CharField(required=False)
    patient_payment_mode = forms.ChoiceField(
        required=False,
        choices=[("insurance", "Insurance"), ("card", "Card"), ("cash", "Cash")]
    )

    # Doctor fields
    doctor_date_of_birth = forms.DateField(required=False, widget=forms.DateInput(attrs={"type": "date"}))
    doctor_mobile_number = forms.CharField(required=False)
    doctor_address = forms.CharField(required=False)
    specialization = forms.CharField(required=False)
    license_number = forms.CharField(required=False)

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if NewUser.objects.filter(email=email).exists():
            raise ValidationError("An account with this email already exists.")
        return email

    def clean(self):
        cleaned = super().clean()
        role = cleaned.get("role")

        if role == "patient":
            required = [
                "patient_date_of_birth",
                "patient_mobile_number",
                "patient_address",
                "patient_payment_mode",
            ]
            mobile = cleaned.get("patient_mobile_number")
            if mobile and Patient.objects.filter(mobile_number=mobile).exists():
                self.add_error("patient_mobile_number", "Mobile already registered.")

        elif role == "doctor":
            required = [
                "doctor_date_of_birth",
                "doctor_mobile_number",
                "doctor_address",
                "specialization",
                "license_number",
            ]
            mobile = cleaned.get("doctor_mobile_number")
            if mobile and Doctor.objects.filter(mobile_number=mobile).exists():
                self.add_error("doctor_mobile_number", "Mobile already registered.")
        else:
            raise ValidationError("Invalid role.")

        for field in required:
            if not cleaned.get(field):
                self.add_error(field, "This field is required.")

        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        #user.username = f"{self.cleaned_data['first_name'].lower()}{uuid.uuid4().hex[:6]}"
        user.role = self.cleaned_data["role"]
        user.is_active = True
        if commit:
            user.save()
            if user.role == "doctor":
                Doctor.objects.create(
                    user=user,
                    date_of_birth=self.cleaned_data["doctor_date_of_birth"],
                    mobile_number=self.cleaned_data["doctor_mobile_number"],
                    address=self.cleaned_data["doctor_address"],
                    specialization=self.cleaned_data["specialization"],
                    license_number=self.cleaned_data["license_number"],
                    is_approved=False,
                )

            elif user.role == "patient":
                Patient.objects.create(
                    user=user,
                    date_of_birth=self.cleaned_data["patient_date_of_birth"],
                    mobile_number=self.cleaned_data["patient_mobile_number"],
                    address=self.cleaned_data["patient_address"],
                    preferred_payment_mode=self.cleaned_data["patient_payment_mode"],
                )

        return user
