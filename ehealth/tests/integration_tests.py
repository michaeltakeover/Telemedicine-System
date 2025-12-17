from django.test import TestCase
from django.urls import reverse
from django.utils.timezone import now
from ehealth.models import NewUser, Patient, Doctor, Appointment

class AppointmentIntegrationTest(TestCase):

    def setUp(self):
        # Create patient user
        self.patient_user = NewUser.objects.create_user(
            email="sarah.collins@testmail.com",
            password="Rk8$L@3vZ!aQ",
            role="patient"
        )
        self.patient = Patient.objects.create(
            user=self.patient_user,
            date_of_birth="2000-01-01",
            mobile_number="0712345678"
        )

        # Create doctor user
        self.doctor_user = NewUser.objects.create_user(
            email="michael.brown@testmail.com",
            password="L!Q8@vT#4xP",
            role="doctor"
        )
        self.doctor = Doctor.objects.create(
            user=self.doctor_user,
            specialization="Cardiology",
            license_number="DOC123",
            is_approved=True
        )

    def test_patient_can_book_appointment(self):
        self.client.login(email="sarah.collins@testmail.com", password="Rk8$L@3vZ!aQ")

        response = self.client.post(
            reverse("ehealth:book_appointment"),
            {
                "doctor": self.doctor.id,
                "appointment_date": now().strftime("%Y-%m-%dT%H:%M"),
                "reason": "Chest pain"
            }
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Appointment.objects.filter(
                patient=self.patient,
                status="pending"
            ).exists()
        )
