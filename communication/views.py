from django.shortcuts import render

# Create your views here.
# communication/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from django.shortcuts import render
from ehealth.models import Consultation, ChatMessage

def consultation_room(request, consultation_id):
    consultation = Consultation.objects.get(id=consultation_id)
    messages = ChatMessage.objects.filter(consultation=consultation)

    return render(request, "communication/consultation_room.html", {
        "consultation": consultation,
        "messages": messages,
    })

'''
@login_required
def messages_inbox(request):
    """Messages inbox"""
    return render(request, 'communication/messages_inbox.html')

@login_required
def chat_room(request, user_id):
    """Chat room"""
    return render(request, 'communication/chat_room.html')

@login_required
def send_message(request, user_id):
    """Send message"""
    return redirect('communication:chat_room', user_id=user_id)

@login_required
def mark_message_read(request, message_id):
    """Mark message as read"""
    return JsonResponse({'status': 'success'})

@login_required
def conversations_list(request):
    """Conversations list"""
    return render(request, 'communication/conversations_list.html')

@login_required
def video_consultation_room(request, appointment_id):
    """Video consultation room"""
    return render(request, 'communication/video_consultation_room.html')

@login_required
def get_video_token(request, appointment_id):
    """Get video token"""
    return JsonResponse({'token': 'dummy_token'})

@login_required
def start_video_call(request, appointment_id):
    """Start video call"""
    return JsonResponse({'status': 'started'})

@login_required
def end_video_call(request, appointment_id):
    """End video call"""
    return JsonResponse({'status': 'ended'})

@login_required
def join_video_call(request, appointment_id):
    """Join video call"""
    return redirect('communication:video_consultation_room', appointment_id=appointment_id)

@login_required
def notifications_list(request):
    """Notifications list"""
    return render(request, 'communication/notifications_list.html')

@login_required
def mark_notification_read(request, notification_id):
    """Mark notification as read"""
    return JsonResponse({'status': 'success'})

@login_required
def mark_all_notifications_read(request):
    """Mark all notifications as read"""
    return JsonResponse({'status': 'success'})

@login_required
def unread_notifications_count(request):
    """Get unread notifications count"""
    return JsonResponse({'count': 0})

@login_required
def shared_files_list(request):
    """Shared files list"""
    return render(request, 'communication/shared_files_list.html')

@login_required
def upload_file(request):
    """Upload file"""
    return redirect('communication:shared_files_list')

@login_required
def file_detail(request, file_id):
    """File detail"""
    return render(request, 'communication/file_detail.html')

@login_required
def download_file(request, file_id):
    """Download file"""
    return redirect('communication:shared_files_list')
'''