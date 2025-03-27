from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _




class UserManager(BaseUserManager):
    #Define a model manager for User model with no username field.

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        #Create and save a User with the given email and password.
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        #Create and save a regular User with the given email and password.
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        #Create and save a SuperUser with the given email and password.
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    #User model.

    username = None
    email = models.EmailField(_('email address'), unique=True)
    
    ROLE_CHOICES = (
        ('job_seeker', 'Job Seeker'),
        ('company', 'Company'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='job_seeker')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()



# ---------------------------------
class PersonalInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Personal Info"

# ---------------------------------
# Education Info Model
# ---------------------------------
class EducationInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    highest_degree = models.CharField(max_length=100, blank=True, null=True)
    university_name = models.CharField(max_length=100, blank=True, null=True)
    passing_year = models.IntegerField(blank=True, null=True)
    grade = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Education Info"

# ---------------------------------
# Job & Project Info Model
# ---------------------------------
class JobInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    current_position = models.CharField(max_length=100, blank=True, null=True)
    company_name = models.CharField(max_length=100, blank=True, null=True)
    years_of_experience = models.IntegerField(blank=True, null=True)
    skills = models.TextField(blank=True, null=True)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Job Info"
