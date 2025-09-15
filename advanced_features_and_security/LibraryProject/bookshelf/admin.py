from django.contrib import admin
from .models import Book
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser




# Register your models here.

class BookAdmin(admin.ModelAdmin):
    list_filter = ('title', 'author', 'publication_year')
    search_fields = ('title', 'author')

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    ordering = ('email',)   # instead of ('username',)


#extends the default UserAdmin fieldsets
    fieldsets = UserAdmin.fieldsets + (
        (None, {"fields":("date_of_birth", "profile_photo")}),
    )

admin.site.register(CustomUser, CustomUserAdmin)


admin.site.register(Book)