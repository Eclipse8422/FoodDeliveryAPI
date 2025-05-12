from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    model = User
    list_display =['id','username', 'email', 'role', 'is_staff', 'is_superuser']
    list_filter=['role']
    fieldsets = UserAdmin.fieldsets + (          # Modifies the edit user page in the admin panel
        ('Choose Role', {'fields': ('role',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (  # Modifies the add user form in the admin panel
        ('Choose Role', {'fields': ('role',)}),
    )

admin.site.register(User, CustomUserAdmin)
