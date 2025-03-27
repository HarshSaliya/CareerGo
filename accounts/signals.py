from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import PersonalInfo, EducationInfo, JobInfo

# Automatically create profile when a user registers
@receiver(post_save, sender=User)
def create_user_profiles(sender, instance, created, **kwargs):
    if created:
        PersonalInfo.objects.create(user=instance)
        EducationInfo.objects.create(user=instance)
        JobInfo.objects.create(user=instance)

# Automatically save profile when user data is updated
@receiver(post_save, sender=User)
def save_user_profiles(sender, instance, **kwargs):
    instance.personalinfo.save()
    instance.educationinfo.save()
    instance.jobinfo.save()
