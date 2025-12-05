from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .models import UserProfile

'''
def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        id_number = request.POST.get("id_number")
        password = request.POST.get("password")

        # Check if user exists by username
        user = authenticate(request, username=username, password=password)

        if user is None:
            return render(request, "userprofile/login.html", {
                "error": "Invalid username or password"
            })

        # Check if ID number matches the same user
        try:
            profile = UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            return render(request, "userprofile/login.html", {
                "error": "Profile not found"
            })

        if profile.id_number != id_number:
            return render(request, "userprofile/login.html", {
                "error": "ID Number does not match this user"
            })

        # 3Login user
        login(request, user)

        # Redirect based on role
        if profile.role == "doctor":
            if not profile.verification_status:
                return render(request, "users_profiles/not_verified.html")
            return redirect("doctor_dashboard")

        if profile.role == "patient":
            return redirect("patient_dashboard")

        return render(request, "users_profiles/login.html", {
            "error": "Unknown user role"
        })

    return render(request, "users_profiles/login.html")

'''

from django.shortcuts import render

def user_login(request):
    return render(request, "users_profiles/login.html")


def register_choice(request):
    return render(request, "users_profiles/register_choice.html")


def register_patient(request):
    return render(request, "users_profiles/patient_register.html")


def register_doctor(request):
    return render(request, "users_profiles/doctor_register.html")
