from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from user.validation import validate_image
import os

class CustomUserManager(BaseUserManager):
   
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(unique=True)
    image = models.ImageField(upload_to='image/user', null=True, blank=True, validators=[validate_image])
    phone = models.CharField(max_length=15, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = CustomUserManager()

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
    
    def __str__(self):
        return f"{self.name} ({self.email})"
    
    def save(self, *args, **kwargs):
        # Check if this is an update to an existing UserProfile instance
        if self.pk:
            # Get the original instance from the database
            data = User.objects.get(pk=self.pk)

            # Check if the profile_image field has changed
            if data.image and data.image != self.image:
                # Delete the old image file
                os.remove(data.image.path)

        super(User, self).save(*args, **kwargs)

