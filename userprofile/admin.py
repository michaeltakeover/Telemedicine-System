from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        "last_name",
        "first_name",
        "mobile_number",
        "role",
        "id_number",
        "verification_status",
    )

    list_filter = ("role", "verification_status")

    search_fields = (
        "user__username",
        "user__first_name",
        "user__last_name",
        "mobile_phone",
        "id_number",
        "role",
        "user__email",
        "specialization"
    )

    # Display First and Last Name from the linked User model
    def first_name(self, obj):
        return obj.user.first_name

    def last_name(self, obj):
        return obj.user.last_name

    # Display mobile number using the field 'phone'
    def mobile_number(self, obj):
        return obj.phone

    # Rename column headers
    first_name.short_description = "First Name"
    last_name.short_description = "Last Name"
    mobile_number.short_description = "Mobile Number"
