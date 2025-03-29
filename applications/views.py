from django.shortcuts import render,redirect
from django.contrib import messages
from .models import Application

def application(request):
    if request.method == 'POST':
        job_id = request.POST['job_id']
        job = request.POST['job']
        creator = request.POST['creator']
        creator_id = request.POST['creator_id']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        resume = request.FILES['resume']
        user_id = request.POST['user_id']

        #  Check if user has made inquiry already
        if request.user.is_authenticated:
            user_id = request.user.id
            has_contacted = Application.objects.all().filter(job_id=job_id, user_id=user_id)
            if has_contacted:
                messages.error(request, 'You have already applied for this job')
                return redirect('/jobs/'+job_id)    

        apply = Application(job=job, job_id=job_id,creator=creator,creator_id=creator_id, name=name, email=email, phone=phone,resume=resume, user_id=user_id)

        apply.save()


        messages.success(request, 'Your application has been submitted')
        return redirect('/jobs/'+ job_id)



from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.db.models import Count
from jobs.models import Job
from applications.models import Application

@login_required
def company_dashboard(request):
    # Ensure only company users can access
    if request.user.role != 'company':
        messages.error(request, 'Access denied. Company accounts only.')
        return redirect('dashboard')

    # Get jobs created by the logged-in company
    jobs = Job.objects.filter(creator=request.user).annotate(
        application_count=Count('applications')
    )

    # Get recent applications for jobs created by this company
    recent_applications = Application.objects.filter(
        job__creator=request.user  # Filter applications related to the company's jobs
    ).order_by('-contact_date')[:10]

    context = {
        'jobs': jobs,
        'recent_applications': recent_applications
    }
    return render(request, 'accounts/company_dashboard.html', context)

@login_required
def job_applications(request, job_id):
    # Ensure the job belongs to the logged-in company
    job = get_object_or_404(Job, id=job_id, creator=request.user)
    applications = Application.objects.filter(job=job)

    context = {
        'job': job,
        'applications': applications
    }
    return render(request, 'accounts/job_applications.html', context)

@login_required
def update_application_status(request, application_id):
    if request.method == 'POST':
        application = get_object_or_404(Application, id=application_id)

        # Ensure only the job creator (company) can update the status
        if application.job.creator != request.user:
            return JsonResponse({'error': 'Unauthorized'}, status=403)

        new_status = request.POST.get('status')
        if new_status:
            application.status = new_status
            application.save()
            return JsonResponse({'success': True})

        return JsonResponse({'error': 'Invalid status'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)
