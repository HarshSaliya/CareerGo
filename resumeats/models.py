from django.db import models
from django.conf import settings
import uuid


class Resume(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="resumes"
    )
    profession = models.CharField(
        max_length=100,
        choices=[
            ("Python Backend", "Python Backend"),
            ("Frontend", "Frontend"),
            ("Java Backend", "Java Backend"),
            ("Data Science", "Data Science"),
            ("PHP", "PHP"),
        ]
    )
    experience_level = models.CharField(
        max_length=50,
        choices=[
            ("Fresher", "Fresher"),
            ("Intermediate", "Intermediate"),
            ("Experienced", "Experienced"),
        ]
    )
    
    resume_file = models.FileField(upload_to="resumes/%Y/%m/%d/")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    score = models.IntegerField(null=True, blank=True)
    feedback = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.first_name} - {self.profession}"



class DummyCreditCard(models.Model):
    card_number = models.CharField(max_length=16, unique=True)  # 16-digit card number
    card_holder = models.CharField(max_length=100)  # Name on card
    expiry_date = models.CharField(max_length=5)  # MM/YY format
    cvv = models.CharField(max_length=3)  # CVV code
    balance = models.DecimalField(max_digits=10, decimal_places=2)  # Available balance

    def __str__(self):
        return f"{self.card_holder} - {self.card_number}"

class Plan(models.Model):
    PLAN_CHOICES = [
        ('3_months', '3 Months'),
        ('6_months', '6 Months'),
        ('1_year', '1 Year'),
    ]

    name = models.CharField(max_length=20, choices=PLAN_CHOICES, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Base price before GST

    def __str__(self):
        return self.name
    
class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    base_price = models.DecimalField(max_digits=8, decimal_places=2)  # Plan price
    gst = models.DecimalField(max_digits=8, decimal_places=2)  # 18% GST
    total_amount = models.DecimalField(max_digits=8, decimal_places=2)  # Final price
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('success', 'Success'), ('failed', 'Failed')], default='pending')
    transaction_id = models.CharField(max_length=100, unique=True, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.plan.name} - {self.status}"