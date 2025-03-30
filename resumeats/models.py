from django.db import models
from django.conf import settings

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
        return f"{self.user.username} - {self.profession}"
