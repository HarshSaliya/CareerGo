# forms.py
from django import forms
from .models import Job

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = [
            'company', 'title', 'role', 'location', 'description', 'about',
            'contract', 'vacancy', 'experience', 'salary', 'deadline', 'main_image'
        ]
        widgets = {
            'deadline': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
