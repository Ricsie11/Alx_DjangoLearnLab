from django.db import models
from django.contrib.auth.models import  AbstractUser, BaseUserManager

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_year = models.IntegerField()



    class meta:
        permissions = [
            ("can_view", "can view"),
            ("can_create", "can create"),    # I created permissions for the Book class, for view, create, edit and delete
            ("can_edit", "can edit"),
            ("can_delete", "can delete"),
        ]


class CustomUserManager(BaseUserManager):
    def create_user (self, email, password=None, **extra_fields):
        if not email:
            raise ValueError ("The email field is required.")
        email = self.normalize_email(email)
        user = self.model (email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser (self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError ("User should have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError ("User should have is_superuser=True.")
        
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    username = None #..................Username is set to None because we want to use email as the login criteria

    #Enforce unique email
    email = models.EmailField(unique=True)

    date_of_birth = models.DateField(null=True, blank=True)
    profile_photo = models.ImageField(upload_to='', null=True, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'  # now email is used for login
    REQUIRED_FIELDS = []   # you can add others if you want them required (e.g. ["date_of_birth"])

