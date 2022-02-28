from django.db import models
from django.contrib.auth.models import AbstractBaseUser,\
     PermissionsMixin   # We need these to customize Django user model
from django.contrib.auth.models import BaseUserManager # To custom user manager

from django.conf import settings    # retrieve setting in our project settings

class UserProfileManager(BaseUserManager):
    """
    Manager for user profiles.
    We custom user manager, we need to define create_user and create_superuser function.
    """

    # Function to create new user
    def create_user(self, email, name, password=None):
        """
        Create a new user profile
        """
        if not email:
            raise ValueError('User must have an email address')
        
        # Because we use email as username, need to normalize email address
        email = self.normalize_email(email)
        user = self.model(email=email, name=name)

        user.set_password(password)
        # Django can support multiple database,
        # it's best practice to specify the database by 'using'
        user.save(using=self._db)

        return user
    
    def create_superuser(self, email, name, password):
        """
        Create and save a new superuser with given details
        """
        user = self.create_user(email, name, password)
        
        user.is_superuser = True
        user.is_staff = True
        # Save model
        user.save(using=self._db)

        return user

# We are customize default user model base on AbstractBaseUser and PermissionsMixin
class UserProfile(AbstractBaseUser, PermissionsMixin):
    """
    Database model for users in the system.
    """
    # Fields we want to include in our model
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)   # Whether they should have access to Django admin

    # Because we customise user model, we need to define User manager 
    # and assign User manager to objects
    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        """
        Retrieve full name of user
        """
        return self.name

    def get_short_name(self):
        """
        Retrieve short name of user
        """
        return self.name

    def __str__(self) -> str:
        """
        Return string representation of user
        """
        return self.email


class ProfileFeedItem(models.Model):
    """
    Profile status update
    """
    user_profile = models.ForeignKey(
        # Best practice to retrieve User model from settings
        # rather than hardcode model, Explanation: video
        settings.AUTH_USER_MODEL,
        # when user is deleted => feeds will be deleted.
        on_delete=models.CASCADE
    )
    status_text = models.CharField(
        max_length=255
    )
    # Every time we create a new feed item => automatically add timestamp
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        """
        Return the model as string
        """
        return self.status_text