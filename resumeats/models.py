from django.db import models

class Resume(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    profession = models.CharField(
        max_length=100,
        choices=[
            ("Python Backend", "Python Backend"),
            ("Frontend", "Frontend"),
            ("Java Backend", "Java Backend"),
            ("Data Science", "Data Science"),
            ("PHP", "PHP"),
            # Add more professions as needed
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
    resume_file = models.FileField(upload_to="media/resumes")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    score = models.IntegerField(null=True, blank=True)
    feedback = models.TextField(blank=True)
