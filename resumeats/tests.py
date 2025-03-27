from django.db import models
from django.contrib.auth.models import AbstractUser

# Extend the default User model to include additional fields
class User(AbstractUser):
    is_employer = models.BooleanField(default=False)
    is_job_seeker = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)

    def __str__(self):
        return self.username

# Company model to store employer details
class Company(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='company')
    name = models.CharField(max_length=255)
    address = models.TextField()
    website = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)

    def __str__(self):
        return self.name

# JobCategory model to categorize job postings
class JobCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# Job model to store job postings
class Job(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='jobs')
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    employment_type = models.CharField(max_length=50, choices=[
        ('Full-Time', 'Full-Time'),
        ('Part-Time', 'Part-Time'),
        ('Contract', 'Contract'),
        ('Freelance', 'Freelance'),
        ('Internship', 'Internship'),
    ])
    salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    posted_at = models.DateTimeField(auto_now_add=True)
    application_deadline = models.DateTimeField()
    category = models.ForeignKey(JobCategory, on_delete=models.SET_NULL, null=True, related_name='jobs')
    required_skills = models.ManyToManyField('Skill', blank=True)

    def __str__(self):
        return f"{self.title} at {self.company.name}"

# Skill model to define various skills
class Skill(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# Application model to track job applications
class Application(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    resume = models.FileField(upload_to='resumes/')
    cover_letter = models.TextField(blank=True, null=True)
    applied_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=[
        ('Applied', 'Applied'),
        ('Reviewed', 'Reviewed'),
        ('Interviewed', 'Interviewed'),
        ('Offered', 'Offered'),
        ('Rejected', 'Rejected'),
    ], default='Applied')

    def __str__(self):
        return f"Application by {self.applicant.username} for {self.job.title}"

class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} - {self.subject}"

# Education model to store applicant's educational background
class Education(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='educations')
    institution = models.CharField(max_length=255)
    degree = models.CharField(max_length=255)
    field_of_study = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    grade = models.CharField(max_length=10, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.degree} in {self.field_of_study} from {self.institution}"

# Experience model to store applicant's work experience
class Experience(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='experiences')
    job_title = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    location = models.CharField(max_length=255, blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.job_title} at {self.company_name}"
