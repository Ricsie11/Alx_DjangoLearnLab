from django.db import models
from django.contrib.auth.models import User, AbstractUser, BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings


# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    

    class Meta:
        permissions = [
            ("can_add_book", "Can add book"),
            ("can_change_book", "Can change book"),
            ("can_delete_book", "Can delete book"),
        ]
    
class Library(models.Model):
    name = models.CharField(max_length=100)
    books = models.ManyToManyField(Book)

    def __str__(self):
        return self.name
    
class Librarian(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, #links to CustomUser
     on_delete=models.CASCADE)
    library = models.OneToOneField(Library, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.email # or self.user.get_full_name()


class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Librarian', 'Librarian'),
        ('Member', 'Member'),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Member')

    def __str__(self):
        return f"{self.user.username} - {self.role}"


# Signal to automatically create a UserProfile whenever a new User is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


# Signal to save profile whenever User is saved
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()


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