from django import forms
from .models import Resume

class ResumeUploadForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ["name", "email", "profession", "experience_level", "resume_file"]
