from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.urls import reverse
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from ..forms.auth import CombinedRegistrationForm
from ..models import NewUser



def register(request):
    """
    Handles new user registration.
    registration requests using the CombinedRegistrationForm.
    and constructs an email-based activation link for account verification.
    """
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

           # send_mail(
             #   subject="Activate Your Telemedicine Account",
              #  message=f"Hello {user.first_name},\n\nActivate your account:\n{activation_link}",
             #   from_email="noreply@telemedicine.com",
              #  recipient_list=[user.email],
           # )

            messages.success(request, "Check your email to activate your account.")
            return redirect("ehealth:login")

    else:
        form = CombinedRegistrationForm()

    return render(request, "ehealth/register.html", {"form": form})



def activate_account(request, uid, token):
    """
    Activates a newly registered user account.
    """
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

    messages.error(request, "Recheck.")
    return redirect("ehealth:register")




def user_login(request):
    """
    Authenticates users and redirects them based on role.
    verifies user credentials, checks account activation status,
    enforces doctor approval requirements, and redirects authenticated
    users to their respective dashboards.
    """
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, email=email, password=password)

        if not user:
            messages.error(request, "Invalid email or password")
            return redirect("ehealth:login")

        if not user.is_active:
            messages.error(request, "Account not activated.")
            return redirect("ehealth:login")

        if user.role == "doctor":
            if not hasattr(user, "doctor") or not user.doctor.is_approved:
                messages.error(request, "Doctor account pending approval.")
                return redirect("ehealth:login")

        login(request, user)

        if user.role == "patient":
            return redirect("ehealth:patient_dashboard")
        elif user.role == "doctor":
            return redirect("ehealth:doctor_dashboard")

        return redirect("ehealth:home")

    return render(request, "ehealth/login.html")




