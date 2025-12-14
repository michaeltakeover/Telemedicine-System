from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from .forms import CombinedRegistrationForm, AppointmentBookingForm,VitalSignForm




from .forms import CombinedRegistrationForm
from .models import NewUser, Patient, Doctor, Appointment, Consultation


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
            return redirect("ehealth:login")

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
        "approved_appointments": appointments.filter(status="approved"),
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
        return redirect("ehealth:home")

    appointments = Appointment.objects.filter(
        patient=patient
    ).order_by("-appointment_date")

    context = {
        "patient": patient,
        "appointments": appointments,
        "vitals": patient.vitals.order_by("-created_at")[:5],
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




from django.shortcuts import get_object_or_404
from .models import Consultation

@login_required
def approve_appointment(request, appointment_id):
    if request.user.role != "doctor":
        messages.error(request, "Access denied.")
        return redirect("ehealth:home")

    appointment = get_object_or_404(Appointment, id=appointment_id)

    if appointment.doctor != request.user.doctor:
        messages.error(request, "You cannot approve this appointment.")
        return redirect("ehealth:doctor_dashboard")

    appointment.status = "approved"
    appointment.save()

    Consultation.objects.get_or_create(
        appointment=appointment,
        defaults={"consultation_type": "chat"}
    )

    messages.success(request, "Appointment approved.")
    return redirect("ehealth:doctor_dashboard")


@login_required
def complete_appointment(request, appointment_id):

    if request.user.role != "doctor":
        messages.error(request, "Access denied.")
        return redirect("ehealth:home")

    try:
        doctor = request.user.doctor
    except Exception:
        messages.error(request, "Doctor profile not found.")
        return redirect("ehealth:home")

    appointment = get_object_or_404(
        Appointment,
        id=appointment_id,
        doctor=doctor   # 🔐 ownership enforced here
    )

    appointment.status = "completed"
    appointment.save()

    messages.success(request, "Appointment marked as completed.")
    return redirect("ehealth:doctor_dashboard")

@login_required
def add_vitals(request):
    if request.user.role != "patient":
        messages.error(request, "Access denied.")
        return redirect("ehealth:home")

    patient = request.user.patient

    if request.method == "POST":
        form = VitalSignForm(request.POST)
        if form.is_valid():
            vital = form.save(commit=False)
            vital.patient = patient
            vital.save()
            messages.success(request, "Vitals recorded successfully.")
            return redirect("ehealth:patient_dashboard")
    else:
        form = VitalSignForm()

    return render(
        request,
        "ehealth/add_vitals.html",
        {"form": form}
    )


@login_required
def doctor_appointment_detail(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)

    if request.user.role != "doctor":
        messages.error(request, "Access denied.")
        return redirect("ehealth:home")

    if appointment.doctor != request.user.doctor:
        messages.error(request, "Access denied.")
        return redirect("ehealth:doctor_dashboard")

    patient = appointment.patient
    vitals = patient.vitals.order_by("-created_at")

    context = {
        "appointment": appointment,
        "patient": patient,
        "vitals": vitals,
    }

    return render(
        request,
        "ehealth/doctor_appointment_detail.html",
        context
    )



from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect

from .models import Appointment, Consultation, ChatMessage


@login_required
def consultation_chat(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)

    # Allow BOTH doctor and patient
    if request.user not in [
        appointment.doctor.user,
        appointment.patient.user
    ]:
        return HttpResponseForbidden("Access denied")

    consultation, _ = Consultation.objects.get_or_create(
        appointment=appointment,
        defaults={"consultation_type": "chat"}
    )

    messages_qs = ChatMessage.objects.filter(
        consultation=consultation
    ).order_by("timestamp")

    is_read_only = appointment.status == "completed"

    if request.method == "POST" and not is_read_only:
        message_text = request.POST.get("message")
        if message_text:
            ChatMessage.objects.create(
                consultation=consultation,
                sender=request.user,
                message=message_text
            )

    return render(
        request,
        "ehealth/consultation_chat.html",
        {
            "appointment": appointment,
            "consultation": consultation,
            "messages": messages_qs,
            "is_read_only": is_read_only,
        }
    )


from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect

from .models import Appointment, Consultation, Prescription
from .forms import PrescriptionForm


@login_required
def create_prescription(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)

    if (
            request.user.role != "doctor"
            or appointment.doctor is None
            or request.user.id != appointment.doctor.user.id
            or appointment.status != "completed"
    ):
            return HttpResponseForbidden("Access denied")

    consultation = appointment.consultation



    if request.method == "POST":
        form = PrescriptionForm(request.POST)
        if form.is_valid():
            prescription = form.save(commit=False)
            prescription.consultation = consultation
            prescription.doctor = appointment.doctor
            prescription.save()

            #return redirect("ehealth:doctor_dashboard")
            return redirect(
                "ehealth:view_prescriptions",
                appointment_id=appointment.id)


    else:
        form = PrescriptionForm()

    return render(request, "ehealth/create_prescription.html", {
        "appointment": appointment,
        "form": form,
    })

@login_required
def save_notes(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)

    # Security: only the assigned doctor can save notes
    if (request.user != appointment.doctor.user
        or appointment.status != "completed"):
        messages.error(request, "Access denied.")
        return redirect("ehealth:doctor_dashboard")
    consultation = appointment.consultation

    if request.method == "POST":
        consultation = appointment.consultation
        consultation.notes = request.POST.get("notes", "").strip()
        consultation.save()
        messages.success(request, "Notes saved successfully.")

    return redirect("ehealth:doctor_dashboard")

@login_required
def view_prescriptions(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    consultation = appointment.consultation

    if request.user not in [appointment.doctor.user, appointment.patient.user]:
        return HttpResponseForbidden("Access denied")
    consultation = appointment.consultation
    prescriptions = consultation.prescriptions.all()

    return render(request,"ehealth/view_prescriptions.html", {
        "appointment": appointment,
        "prescriptions": prescriptions,
    })
