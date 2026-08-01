from django.contrib import admin

from .models import faculty, users_profile


@admin.register(users_profile)
class UsersProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user_id",
        "user_name",
        "user_short_name",
        "role",
        "isadmin",
        "user_status",
    )
    list_filter = ("role", "isadmin")
    search_fields = ("user_name", "user_short_name", "user_email")
    list_editable = ("role", "isadmin")


@admin.register(faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ("faculty_id", "faculty_ar_name", "faculty_en_name")
    search_fields = ("faculty_ar_name", "faculty_en_name")
