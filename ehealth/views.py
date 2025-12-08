from django.shortcuts import render

# Create your views here.
# ehealth/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render


def home(request):
   return render(request,'ehealth/home.html')

def login(request):
    return render(request,'ehealth/login.html')


def Support(request):
    return render(request,'ehealth/Support.html')

def register(request):
    return render(request, "ehealth/register.html")
