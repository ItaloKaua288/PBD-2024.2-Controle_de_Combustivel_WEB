from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuarios

class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "password", "cargo", "groups")}),
        (("Permissions"), {"fields": ("is_superuser",),},),
    )
    list_display = ("username",)
    list_filter = ("is_superuser",)

admin.site.register(Usuarios, CustomUserAdmin)