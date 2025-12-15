
from django.test import TestCase
from datetime import date
from ehealth.models import NewUser, Patient, Doctor


class UserModelTests(TestCase):

    def test_create_patient_user(self):
        user = NewUser.objects.create_user(
            email="grace.patel@testmail.com",
            password="!P9QZ@xK#7L",
            role="patient"
        )
        self.assertEqual(user.email, "grace.patel@testmail.com")
        self.assertTrue(user.check_password("!P9QZ@xK#7L"))

    def test_user_role_is_saved(self):
        user = NewUser.objects.create_user(
            email="noah.kim@testmail.com",
            password="Q#Z!P9x@K7L",
            role="doctor"
        )
        self.assertEqual(user.role, "doctor")


class ProfileModelTests(TestCase):

    def test_patient_profile_creation(self):
        user = NewUser.objects.create_user(
            email="grace.patel@testmail.com",
            password="!P9QZ@xK#7L",
            role="patient"
        )
        patient = Patient.objects.create(
            user=user,
            date_of_birth=date(2000, 1, 1),
            mobile_number="123456789",
            address="Test",
            preferred_payment_mode="cash"
        )
        self.assertEqual(patient.user.email, "grace.patel@testmail.com")

    def test_doctor_profile_not_approved_by_default(self):
        user = NewUser.objects.create_user(
            email="noah.kim@testmail.com",
            password="Q#Z!P9x@K7L",
            role="doctor"
        )
        doctor = Doctor.objects.create(
            user=user,
            date_of_birth=date(1980, 1, 1),
            mobile_number="987654321",
            address="Test",
            specialization="General",
            license_number="LIC123"
        )
        self.assertFalse(doctor.is_approved)

# One User One Profile
class RelationshipTests(TestCase):

    def test_user_has_patient_profile(self):
        user = NewUser.objects.create_user(
            email="grace.patel@testmail.com",
            password="!P9QZ@xK#7L",
            role="patient"
        )

        patient = Patient.objects.create(
            user=user,
            date_of_birth=date(2000, 1, 1),
            mobile_number="123456789",
            address="Test",
            preferred_payment_mode="cash"
        )

        self.assertEqual(patient.user, user)
