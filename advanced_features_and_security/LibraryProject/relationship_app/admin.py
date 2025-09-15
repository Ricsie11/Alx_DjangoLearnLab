from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# Register your models here.

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    ordering = ('email',)   # instead of ('username',)


#extends the default UserAdmin fieldsets
    fieldsets = UserAdmin.fieldsets + (
        (None, {"fields":("date_of_birth", "profile_photo")}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
