"""
Models responsible for messages and notifications
within the telemedicine system.
"""
from django.db import models
from django.conf import settings
from .records import Consultation
import uuid


class ChatMessage(models.Model):
    """
    Represents a single chat message exchanged between
    a doctor and a patient during a consultation session.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    consultation = models.ForeignKey(Consultation, on_delete=models.CASCADE)
    #sender = models.ForeignKey(User, on_delete=models.CASCADE)  # doctor or patient
    sender = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)

    message = models.TextField()

    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender.email} at  {self.timestamp}"



class Notification(models.Model):
    """
    Represents  notifications
    sent for appointment updates).
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    #user = models.ForeignKey(User, on_delete=models.CASCADE)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="sent_notifications")
    receiver = models.ForeignKey( settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="received_notifications" )

    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for  {self.receiver.email}"

