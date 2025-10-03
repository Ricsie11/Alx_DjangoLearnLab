from django.contrib import admin
from .models import Post, CustomUser

# Register your models here.
admin.site.register(Post)
admin.site.register(CustomUser)
