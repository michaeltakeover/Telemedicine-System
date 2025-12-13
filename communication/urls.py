from django.urls import path
from . import views

app_name = "communication"

urlpatterns = [
    path("consultation/<uuid:consultation_id>/", views.consultation_room, name="consultation_room"),
]
