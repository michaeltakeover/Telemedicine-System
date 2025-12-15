from django.shortcuts import render

def support(request):
    return render(request, "ehealth/support.html")
