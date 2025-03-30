from django.shortcuts import render,redirect
from django.contrib import messages
from .models import Application
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from jobs.models import Job

def application(request):
    if request.method == 'POST':
        job_id = request.POST.get('job_id')
        job = get_object_or_404(Job, id=job_id)
        
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        resume = request.FILES.get('resume')  # Optional file upload
        cover_letter = request.POST.get('cover_letter', '').strip()
        portfolio_url = request.POST.get('portfolio_url', '').strip()
        linkedin_profile = request.POST.get('linkedin_profile', '').strip()
        github_profile = request.POST.get('github_profile', '').strip()
        expected_salary = request.POST.get('expected_salary', None)
        available_start_date = request.POST.get('available_start_date', None)

        # Ensure authenticated user
        if request.user.is_authenticated:
            user_id = request.user.id
            has_applied = Application.objects.filter(job=job, applicant_id=user_id).exists()
            if has_applied:
                messages.error(request, 'You have already applied for this job.')
                return redirect('/jobs/' + str(job_id))

            # Create Application
            application = Application(
                job=job,
                applicant=request.user,
                name=name,
                email=email,
                phone=phone,
                resume=resume,
                cover_letter=cover_letter,
                portfolio_url=portfolio_url or None,
                linkedin_profile=linkedin_profile or None,
                github_profile=github_profile or None,
                expected_salary=expected_salary or None,
                available_start_date=available_start_date or None,
            )
            application.save()

            messages.success(request, 'Your application has been submitted successfully.')
            return redirect('/jobs/' + str(job_id))
        
        messages.error(request, 'You must be logged in to apply.')
        return redirect('/login/')  # Redirect to login if not authenticated

    return redirect('/jobs/')  # Redirect to job listings if accessed via GET
