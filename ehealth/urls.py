# ehealth/urls.py

from django.urls import path
from  .import views


app_name = 'ehealth'

urlpatterns = [

    #path('admin/', admin.site.urls, name='admin.site.urls'),
    # path('home/', views.home),
    path('login/', views.login),
    path('Support/',views.Support),
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),

]