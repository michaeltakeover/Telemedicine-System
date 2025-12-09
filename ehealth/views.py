

# Create your views here.
# ehealth/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render
from .forms import CombinedRegistrationForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import NewUser


def home(request):
   return render(request,'ehealth/home.html')

def user_login(request):
    return render(request,'ehealth/login.html')


def Support(request):
    return render(request,'ehealth/Support.html')

# def register(request,pk):
   # return render(request, "ehealth/register.html")

from .forms import CombinedRegistrationForm
from .models import NewUser


def register(request):
    if request.method == "POST":
        form = CombinedRegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()
            user.is_active = False  # disable until email activation
            user.save()

            # generate uidb64 + token
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)


            activation_link = request.build_absolute_uri(
                reverse("ehealth:activate", kwargs={"uid": uidb64, "token": token})

            )

            # send activation email
            send_mail(
                subject="Activate Your Telemedicine Account",
                message=f"Hello {user.first_name},\n\n"
                        f"Click the link below to activate your account:\n{activation_link}",
                from_email="noreply@telemedicine.com",
                recipient_list=[user.email],
            )

            messages.success(request,
                "Your account has been created. Please check your email to activate your account."
            )
            form = CombinedRegistrationForm()  # clears form fields
            return render(request, "ehealth/register.html", {"form": form})


        else:
            messages.error(request, "There were errors in your form. Please correct them.")
    else:
        form = CombinedRegistrationForm()

    return render(request, "ehealth/register.html", {"form": form})


def activate_account(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = NewUser.objects.get(pk=uid)
    except:
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Account activated! You can now log in.")
        return redirect("ehealth:login")
    if user.role == "patient" and not hasattr(user, "patient"):
        Patient.objects.create(user=user)



    else:
        messages.error(request, "Activation link is invalid or expired.")
        return redirect("ehealth:register")



def user_login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Authenticate using email field
        user = authenticate(request, email=email, password=password)

        if user is None:
            messages.error(request, "Invalid email or password")
            return redirect("ehealth:login")

        if not user.is_active:
            messages.error(request, "Your account is not activated. Check your email.")
            return redirect("ehealth:login")

        # Doctor approval check
        if user.role == "doctor":
            doctor = getattr(user, "doctor", None)
            if doctor and not doctor.is_approved:
                messages.error(request, "Doctor account pending admin approval.")
                return redirect("ehealth:login")

        # Login the user
        login(request, user)
        messages.success(request, "Login successful!")

        # Redirect based on role
        if user.role == "doctor":
            return redirect("ehealth:doctor_dashboard")

        elif user.role == "patient":
            return redirect("ehealth:patient_dashboard")

        # Default for admin or other roles
        return redirect("ehealth:home")

    # GET request → show login page
    return render(request, "ehealth/login.html")




def user_login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Authenticate using email field
        user = authenticate(request, email=email, password=password)

        if user is None:
            messages.error(request, "Invalid email or password")
            return redirect("ehealth:login")

        if not user.is_active:
            messages.error(request, "Your account is not activated. Check your email.")
            return redirect("ehealth:login")

        # Doctor approval check
        if user.role == "doctor":
            doctor = getattr(user, "doctor", None)
            if doctor and not doctor.is_approved:
                messages.error(request, "Doctor account pending admin approval.")
                return redirect("ehealth:login")

        # Login the user
        login(request, user)
        messages.success(request, "Login successful!")

        # Redirect based on role
        if user.role == "doctor":
            return redirect("ehealth:doctor_dashboard")

        elif user.role == "patient":
            return redirect("ehealth:patient_dashboard")

        # Default for admin or other roles
        return redirect("ehealth:home")

    # GET request → show login page
    return render(request, "ehealth/login.html")







# Dash boards

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

@login_required
def patient_dashboard(request):
    if request.user.role != "patient":
        return redirect("ehealth:home")

    patient = request.user.patient

    context = {
        "patient": patient,
        "upcoming_appointments": patient.appointments.filter(status="pending").order_by("scheduled_time")[:5],
        "past_appointments": patient.appointments.filter(status="completed").order_by("-scheduled_time")[:5],
        "vitals": patient.vitals.order_by("-recorded_at")[:5],
        "medical_records": patient.medical_records.order_by("-created_at")[:5],
    }

    return render(request, "ehealth/patient_dashboard.html", context)
# Doctor
@login_required
def doctor_dashboard(request):
    if request.user.role != "doctor":
        return redirect("ehealth:home")

    doctor = request.user.doctor

    context = {
        "doctor": doctor,
        "assigned_patients": doctor.patients.all(),
        "pending": doctor.appointments.filter(status="pending").order_by("scheduled_time")[:5],
        "upcoming": doctor.appointments.filter(status="pending", scheduled_time__gte=timezone.now()),
        "completed": doctor.appointments.filter(status="completed").order_by("-scheduled_time")[:5],
    }

    return render(request, "ehealth/doctor_dashboard.html", context)
