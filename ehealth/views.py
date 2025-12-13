from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from .forms import CombinedRegistrationForm, AppointmentBookingForm

from django.utils import timezone


from .forms import CombinedRegistrationForm
from .models import NewUser, Patient, Doctor, Appointment, VitalSign


def home(request):
    return render(request, "ehealth/home.html")

def support(request):
    return render(request, "ehealth/support.html")



def register(request):
    if request.method == "POST":
        form = CombinedRegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()
            user.is_active = True
            user.save()

            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)

            activation_link = request.build_absolute_uri(
                reverse("ehealth:activate", kwargs={"uid": uidb64, "token": token})
            )

            send_mail(
                subject="Activate Your Telemedicine Account",
                message=f"Hello {user.first_name},\n\nActivate your account:\n{activation_link}",
                from_email="noreply@telemedicine.com",
                recipient_list=[user.email],
            )

            messages.success(request, "Check your email to activate your account.")
            return redirect("ehealth:login")

    else:
        form = CombinedRegistrationForm()

    return render(request, "ehealth/register.html", {"form": form})


def activate_account(request, uid, token):
    try:
        user = NewUser.objects.get(pk=urlsafe_base64_decode(uid).decode())
    except NewUser.DoesNotExist:
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(
            request,
            "Account activated. Doctors require admin approval before login."
        )
        return redirect("ehealth:login")

    messages.error(request, "Activation link is invalid.")
    return redirect("ehealth:register")




def user_login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, email=email, password=password)

        if not user:
            messages.error(request, "Invalid email or password")
            return redirect("ehealth:login.html")

        if not user.is_active:
            messages.error(request, "Account not activated.")
            return redirect("ehealth:login.html")

        if user.role == "doctor":
            if not hasattr(user, "doctor") or not user.doctor.is_approved:
                messages.error(request, "Doctor account pending approval.")
                return redirect("ehealth:login.html")

        login(request, user)

        if user.role == "patient":
            return redirect("ehealth:patient_dashboard")
        elif user.role == "doctor":
            return redirect("ehealth:doctor_dashboard")

        return redirect("ehealth:home")

    return render(request, "ehealth/login.html")





@login_required
def doctor_dashboard(request):
    if request.user.role != "doctor":
        messages.error(request, "Access denied.")
        return redirect("ehealth:home")


    doctor = request.user.doctor

    appointments = Appointment.objects.filter(doctor=doctor)

    context = {
        "doctor": doctor,
        "pending_appointments": appointments.filter(status="pending")[:5],
        "completed_appointments": appointments.filter(status="completed")[:5],
    }

    return render(request, "ehealth/doctor_dashboard.html", context)



@login_required
def patient_dashboard(request):
    if request.user.role != "patient":
        messages.error(request, "Access denied.")
        return redirect("ehealth:home")
    try:
        patient = request.user.patient

    except Patient.DoesNotExist:
        messages.error(
            request,
            "Your patient profile is incomplete. Please contact support."
        )
        redirect("ehealth:home")

    context = {
        "patient": patient,
        "upcoming_appointments": Appointment.objects.filter(
            patient=patient, status="pending"
        ).order_by("appointment_date")[:5],

        "past_appointments": Appointment.objects.filter(
            patient=patient, status="completed"
        ).order_by("-appointment_date")[:5],

        "vitals": VitalSign.objects.filter(
            patient=patient
        ).order_by("-created_at")[:5],
    }

    return render(request, "ehealth/patient_dashboard.html", context)


@login_required
def book_appointment(request):
    if request.user.role != "patient":
        messages.error(request, "Access denied.")
        return redirect("ehealth:home")

    patient = request.user.patient

    if request.method == "POST":
        form = AppointmentBookingForm(request.POST, patient=patient)

        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = patient
            appointment.status = "pending"

            #
            child = form.cleaned_data.get("child")
            if child and child.parent != patient:
                messages.error(request, "Invalid child selection.")
                return redirect("ehealth:home")

            appointment.save()

            messages.success(request, "Appointment booked successfully.")
            return redirect("ehealth:patient_dashboard")

    else:
        form = AppointmentBookingForm(patient=patient)

    return render(
        request,
        "ehealth/book_appointment.html",
        {"form": form}
    )
