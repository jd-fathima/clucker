"""Configuration of the admini interface for microblogs"""

from django.contrib import admin
from .models import User

@admin.register(User)

class UserAdmin(admin.ModelAdmin):#class for configuring model classes
    """Configuration of the admin interface for users."""
    list_display = [
        'username','first_name','last_name','email','is_active',
    ]
