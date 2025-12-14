from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import NewUser, Patient, Doctor
import uuid


from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import NewUser, Patient, Doctor
import uuid
from django.utils.timezone import now
from .models import VitalSign




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
    # ✅ PATIENT fields
    patient_date_of_birth = forms.DateField(
        required=False,
        widget=forms.DateInput(
            attrs={
                "type": "date",
                "class": "form-control"
            }
        )
    )

    patient_mobile_number = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    patient_address = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    patient_payment_mode = forms.ChoiceField(
        required=False,
        choices=[
            ("insurance", "Insurance"),
            ("card", "Credit/Debit Card"),
            ("cash", "Cash"),
        ],
        widget=forms.Select(attrs={"class": "form-control"})
    )

    # ✅ DOCTOR fields
    doctor_date_of_birth = forms.DateField(
        required=False,
        widget=forms.DateInput(
            attrs={
                "type": "date",
                "class": "form-control"
            }
        )
    )

    doctor_mobile_number = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    doctor_address = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    specialization = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    license_number = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )


    # -------------------------
    # Email validation
    # -------------------------
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if NewUser.objects.filter(email=email).exists():
            raise ValidationError("An account with this email already exists.")
        return email

    # -------------------------
    # Role-based validation
    # -------------------------
    def clean(self):
        cleaned = super().clean()
        role = cleaned.get("role")

        if role == "patient":
            required_fields = [
                "patient_date_of_birth",
                "patient_mobile_number",
                "patient_address",
                "patient_payment_mode",
            ]

            mobile = cleaned.get("patient_mobile_number")
            if mobile:
                if not mobile.isdigit():
                    self.add_error("patient_mobile_number", "Digits only.")
                elif Patient.objects.filter(mobile_number=mobile).exists():
                    self.add_error(
                        "patient_mobile_number",
                        "This mobile number is already registered."
                    )

        elif role == "doctor":
            required_fields = [
                "doctor_date_of_birth",
                "doctor_mobile_number",
                "doctor_address",
                "specialization",
                "license_number",
            ]

            mobile = cleaned.get("doctor_mobile_number")
            if mobile:
                if not mobile.isdigit():
                    self.add_error("doctor_mobile_number", "Digits only.")
                elif Doctor.objects.filter(mobile_number=mobile).exists():
                    self.add_error(
                        "doctor_mobile_number",
                        "This mobile number is already registered."
                    )

        else:
            raise ValidationError("Invalid role selected.")

        for field in required_fields:
            if not cleaned.get(field):
                self.add_error(field, "This field is required.")

        return cleaned

    # -------------------------
    # SAVE (USER ONLY)
    # -------------------------
    def save(self, commit=True):
        user = super().save(commit=False)

        # Generate username
        unique_part = uuid.uuid4().hex[:6]
        user.username = f"{self.cleaned_data['first_name'].lower()}{unique_part}"

        user.role = self.cleaned_data["role"]
        user.is_active = True

        if commit:
            user.save()

        return user

# ehealth/forms.py
from django import forms
from ehealth.models import NewUser

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = NewUser
        fields = ["email", "password", "role", "gender", "first_name", "last_name"]

    def clean_role(self):
        role = self.cleaned_data.get("role")
        if not role:
            raise forms.ValidationError("Role is required")
        return role


from django import forms
from .models import Appointment, ChildProfile, Doctor

from django import forms
from .models import Appointment, Doctor, ChildProfile


class AppointmentBookingForm(forms.ModelForm):
    child = forms.ModelChoiceField(
        queryset=ChildProfile.objects.none(),
        required=False,
        empty_label="For yourself",
        help_text="Select a child if appointment is for your child"
    )

    class Meta:
        model = Appointment
        fields = ["doctor", "child", "appointment_date", "reason"]
        widgets = {
            "appointment_date": forms.DateTimeInput(
                attrs={
                    "type": "datetime-local",
                    "min": now().strftime("%Y-%m-%dT%H:%M")
                }
            ),
            "reason": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        patient = kwargs.pop("patient")
        super().__init__(*args, **kwargs)

        children_qs = ChildProfile.objects.filter(parent=patient)

        if children_qs.exists():
            self.fields["child"].queryset = children_qs
        else:
            #  No children → remove field entirely
            self.fields.pop("child")

        #  Only approved doctors
        self.fields["doctor"].queryset = Doctor.objects.filter(
            is_approved=True
        )


class VitalSignForm(forms.ModelForm):
    class Meta:
        model = VitalSign
        fields = [
            "blood_pressure",
            "heart_rate",
            "temperature",
            "oxygen_level"
        ]

    def save(self, commit=True):
        vital = super().save(commit=False)


        if (
                vital.temperature > 40.0 or
                vital.heart_rate > 150 or
                vital.oxygen_level < 90
        ):
            vital.is_abnormal = True
        else:
            vital.is_abnormal = False

        if commit:
            vital.save()

        return vital

from django import forms
from .models import Prescription

class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ["medication_name", "dosage", "instructions"]
        widgets = {
            "medication_name": forms.TextInput(attrs={"class": "form-control"}),
            "dosage": forms.TextInput(attrs={"class": "form-control"}),
            "instructions": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }

