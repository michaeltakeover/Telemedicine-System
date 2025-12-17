# doctor.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from ..models import Doctor, Appointment

@login_required
def doctor_dashboard(request):
    """
    Display the doctor dashboard.
    Access is restricted to authenticated users with the doctor role.
    """
    if request.user.role != "doctor":
        messages.error(request, "Access denied.")
        return redirect("ehealth:home")

    doctor = request.user.doctor

    if not doctor.is_approved:
        messages.warning(
            request,
            "Your account is pending admin approval."
        )
        return redirect("ehealth:login.html")

    appointments = Appointment.objects.filter(doctor=doctor)

    context = {
        "doctor": doctor,
        "pending_appointments": appointments.filter(status="pending")[:5],
        "approved_appointments": appointments.filter(status="approved"),
        "completed_appointments": appointments.filter(status="completed")[:5],
    }

    return render(request, "ehealth/doctor_dashboard.html", context)



@login_required
def complete_appointment(request, appointment_id):
    """
    Mark an appointment as completed.
    allows the assigned doctor to mark an appointment as completed once the consultation has finished.
    """

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
        doctor=doctor
    )

    appointment.status = "completed"
    appointment.save()

    messages.success(request, "Appointment marked as completed.")
    return redirect("ehealth:doctor_dashboard")


