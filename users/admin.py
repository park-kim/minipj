from django.contrib import admin

from users.models import User


# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        "user_id",
        "email",
        "username",
        "phone_number",
        "last_login",
        "is_staff",
        "is_active",
    ]

    search_fields = ["email", "username", "phone_number"]

    list_filter = ["is_staff", "is_active"]

    readonly_fields = ["is_staff"]
