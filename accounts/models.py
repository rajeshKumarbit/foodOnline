from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, password=None):
        # We need to ensure the user provides an email and username,
        # as these are mandatory and unique fields in our custom User model.
        if not email:
            raise ValueError('User must have an email address')
        if not username:
            raise ValueError("User must have an username")
        
        # Create a new, unsaved User instance and set its initial fields.
        # We use self.normalize_email to ensure a consistent email format.
        user = self.model(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,
        )
        
        # Use Django's built-in set_password() method to hash the password.
        # This is crucial for security, as it prevents storing the password in plain text.
        user.set_password(password)
        
        # Save the new user instance to the database using the same connection
        # as the manager.
        user.save(using=self._db)
        return user
    
    def create_superuser(self, first_name, last_name, username, email, password=None):
        # We start by calling the 'create_user' method. Why do we do this instead of writing the code all over again?
        user = self.create_user(
            email = self.normalize_email(email),
            password=password,
            username = username,
            first_name = first_name,
            last_name = last_name,
        )
        
        # We now need to grant this user special administrative powers. What do these next four lines do?
        # What is the purpose of each one?
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        
        # Finally, we save the user to the database.
        user.save(using=self._db)
        return user



# The User model inherits from Django's AbstractBaseUser to create a custom user.
# This allows us to add fields specific to our application, like 'role'.
class User(AbstractBaseUser):
    # These integer constants represent the two types of users in our application.
    RESTAURANT = 1
    CUSTOMER = 2

    # This tuple provides the human-readable choices for the 'role' field.
    # It links the integer values above to descriptive strings.
    ROLE_CHOICE = (
        (RESTAURANT, 'Restaurant'),
        (CUSTOMER, 'Customer'),
    )
    
    # Custom fields for our user model.
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    # The username is set to be unique and is also used as the primary identifier for login.
    username = models.EmailField(max_length=50, unique=True)
    # The email field is also unique to ensure no two users share the same email.
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=12, blank=True)
    # The role field uses a PositiveSmallIntegerField to store the user's type.
    # 'choices' links it to our ROLE_CHOICE tuple, and 'blank=True, null=True' means it's optional.
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICE, blank=True, null=True)

    # Required fields for a custom user model.
    # auto_now_add=True sets the date only when the user is first created.
    date_joined = models.DateTimeField(auto_now_add=True)
    # This field should be updated on every login.
    last_login = models.DateTimeField(auto_now_add=True)
    # This field is a duplicate of date_joined, but good for clarity.
    created_date = models.DateTimeField(auto_now_add=True)
    # auto_now=True updates the date every time the user object is saved.
    modified_date = models.DateTimeField(auto_now=True)
    
    # Boolean fields that define a user's permissions and status.
    # The 'default=False' ensures a new user has no administrative powers unless manually assigned.
    is_admin = models.BooleanField(default=False)
    # is_staff=True allows a user to log into the Django admin panel.
    is_staff = models.BooleanField(default=False)
    # is_active=True means the user's account is active and can log in.
    is_active = models.BooleanField(default=False)
    is_Superadmin = models.BooleanField(default=False)
    
    # We must specify which field Django should use as the unique identifier for a user.
    USERNAME_FIELD = 'email'
    # We must also specify which fields are required for a user to be created.
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    
    # Connects our User model to the UserManager we created earlier.
    objects = UserManager()

    # The string representation of a User object, useful for the admin panel and debugging.
    def __str__(self):
        return self.email

    # Methods to check for a user's permissions.
    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
    

class UserProfile(models.Model):
    user = models.OneToOneField("User", on_delete= models.CASCADE, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='user/profile_picture', blank=True, null=True)
    cover_photos = models.ImageField(upload_to='user/cover_photo', blank=True, null=True)
    address_line_1 = models.CharField(max_length = 50, blank=True, null=True)
    address_line_2 = models.CharField(max_length = 50, blank=True, null=True)
    country = models.CharField(max_length = 20, blank=True, null=True)
    city = models.CharField(max_length = 20, blank=True, null=True)
    pin_code = models.CharField(max_length = 8, blank=True, null=True)
    latitude = models.CharField(max_length = 25, blank=True, null=True)
    longitude = models.CharField(max_length = 50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email