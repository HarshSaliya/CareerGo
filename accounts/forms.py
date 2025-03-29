from django import forms
from .models import PersonalInfo, EducationInfo, JobInfo

class PersonalInfoForm(forms.ModelForm):
    class Meta:
        model = PersonalInfo
        fields = ['phone', 'address', 'city', 'state', 'country', 'profile_image']

class EducationInfoForm(forms.ModelForm):
    class Meta:
        model = EducationInfo
        fields = ['highest_degree', 'university_name', 'passing_year', 'grade']

class JobInfoForm(forms.ModelForm):
    class Meta:
        model = JobInfo
        fields = ['current_position', 'company_name', 'years_of_experience', 'skills', 'resume']
