# communication/urls.py

from django.urls import path
from . import views

app_name = 'communication'

urlpatterns = [
    # ============================================
    # MESSAGING
    # ============================================

    path('messages/', views.messages_inbox, name='messages_inbox'),
    path('messages/<uuid:user_id>/', views.chat_room, name='chat_room'),
    path('messages/<uuid:user_id>/send/', views.send_message, name='send_message'),
    path('messages/mark-read/<uuid:message_id>/', views.mark_message_read, name='mark_message_read'),
    path('conversations/', views.conversations_list, name='conversations_list'),

    # ============================================
    # VIDEO CONSULTATION
    # ============================================

    path('video-call/<uuid:appointment_id>/', views.video_consultation_room, name='video_consultation_room'),
    path('video-call/<uuid:appointment_id>/token/', views.get_video_token, name='get_video_token'),
    path('video-call/<uuid:appointment_id>/start/', views.start_video_call, name='start_video_call'),
    path('video-call/<uuid:appointment_id>/end/', views.end_video_call, name='end_video_call'),
    path('video-call/<uuid:appointment_id>/join/', views.join_video_call, name='join_video_call'),

    # ============================================
    # NOTIFICATIONS
    # ============================================

    path('notifications/', views.notifications_list, name='notifications_list'),
    path('notifications/<uuid:notification_id>/mark-read/', views.mark_notification_read,
         name='mark_notification_read'),
    path('notifications/mark-all-read/', views.mark_all_notifications_read, name='mark_all_notifications_read'),
    path('notifications/unread-count/', views.unread_notifications_count, name='unread_notifications_count'),

    # ============================================
    # FILE SHARING
    # ============================================

    path('files/', views.shared_files_list, name='shared_files_list'),
    path('files/upload/', views.upload_file, name='upload_file'),
    path('files/<uuid:file_id>/', views.file_detail, name='file_detail'),
    path('files/<uuid:file_id>/download/', views.download_file, name='download_file'),
]