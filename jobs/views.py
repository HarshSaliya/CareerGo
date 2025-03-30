from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import EmptyPage, PageNotAnInteger,Paginator
from .choices import location_choices, contract_choices
from .models import Job 
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from datetime import datetime

# views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Job
from .forms import JobForm


def index(request):
    jobs = Job.objects.order_by('-job_date').filter(is_published = True) # Fetching data from db

    paginator = Paginator(jobs,3) 
    page_number = request.GET.get('page')
    paged_jobs = paginator.get_page(page_number)

    context = {
        'jobs': paged_jobs
    }
    return render (request , 'jobs/jobs.html', context)


def job(request,job_id):
     #If user searches for an invalid job , display a 404 error page

    job = get_object_or_404(Job , pk=job_id)

    context = {
        'job': job
    }

    return render (request , 'jobs/job.html',context)

def search(request):
    job_list = Job.objects.order_by('-job_date')


    if 'role' in request.GET:
        role = request.GET['role']
        if role:
            job_list = job_list.filter(role__icontains = role)


    if 'location' in request.GET:
        location = request.GET['location']
        if location:
           job_list = job_list.filter(location__iexact = location)
     

    if 'contract' in request.GET:
        contract = request.GET['contract']
        if contract:
            job_list = job_list.filter(contract__iexact = contract)


    context = {
        'location_choices': location_choices,
        'contract_choices': contract_choices,
        'jobs': job_list,
        'values': request.GET # preserving form inputs 

    }
    return render (request , 'jobs/search.html',context)

@login_required()
def applyjob(request,job_id):
    job = get_object_or_404(Job , pk=job_id)
    # if deadline >= datetime.now():
    #     messages.error(request, 'Deadline is done')
    #     return redirect('/jobs/'+job_id)    

    context = {
        'job': job
    }
    return render(request,'jobs/applyjob.html',context)




@login_required
def post_job(request):
    # Check if the logged-in user is a company
    if request.user.role == 'company':  # Only company/HR can post
        if request.method == 'POST':
            form = JobForm(request.POST, request.FILES)
            if form.is_valid():
                job = form.save(commit=False)
                job.creator = request.user  # Assign the logged-in user as creator
                job.save()
                messages.success(request, 'Job posted successfully!')
                return redirect('dashboard')  # Redirect to dashboard or job list
        else:
            form = JobForm()
        return render(request, 'jobs/post_job.html', {'form': form})
    else:
        messages.error(request, 'You do not have permission to post jobs.')
        return redirect('dashboard')


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Job
from applications.models import Application
from .forms import JobForm

@login_required
def manage_jobs(request):
    """HR Dashboard to manage posted jobs and applications."""
    if request.user.role != 'company':
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('dashboard')
    
    jobs = Job.objects.filter(creator=request.user)
    
    # Filtering options
    job_title = request.GET.get('title')
    location = request.GET.get('location')
    contract = request.GET.get('contract')
    
    if job_title:
        jobs = jobs.filter(title__icontains=job_title)
    if location:
        jobs = jobs.filter(location=location)
    if contract:
        jobs = jobs.filter(contract=contract)
    
    return render(request, 'jobs/manage_jobs.html', {'jobs': jobs})


@login_required
def job_applications(request, job_id):
    """View applications for a specific job."""
    job = get_object_or_404(Job, id=job_id, creator=request.user)
    applications = Application.objects.filter(job=job)
    
    # Filtering applications
    status = request.GET.get('status')
    if status:
        applications = applications.filter(status=status)
    
    return render(request, 'jobs/job_applications.html', {'job': job, 'applications': applications})


@login_required
def edit_job(request, job_id):
    """Edit an existing job posting."""
    job = get_object_or_404(Job, id=job_id, creator=request.user)
    
    if request.method == 'POST':
        form = JobForm(request.POST, request.FILES, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, 'Job updated successfully!')
            return redirect('manage_jobs')
    else:
        form = JobForm(instance=job)
    
    return render(request, 'jobs/edit_job.html', {'form': form, 'job': job})


@login_required
def delete_job(request, job_id):
    """Delete a job posting."""
    job = get_object_or_404(Job, id=job_id, creator=request.user)
    job.delete()
    messages.success(request, 'Job deleted successfully!')
    return redirect('manage_jobs')


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from jobs.models import Job
from applications.models import Application

@login_required
def job_applications(request, job_id):
    job = get_object_or_404(Job, id=job_id, creator=request.user)  # Ensure HR can only view their jobs
    applications = Application.objects.filter(job=job)  # Get all applications for this job

    # Optional: Filter by status (Pending, Reviewed, Accepted, Rejected)
    status_filter = request.GET.get('status')
    if status_filter in dict(Application.STATUS_CHOICES):
        applications = applications.filter(status=status_filter)
        
     # ✅ Pagination (10 applications per page)
    paginator = Paginator(applications, 10)  # Show 10 applications per page
    page_number = request.GET.get('page')
    applications_page = paginator.get_page(page_number)  # Get paginated applications


    return render(request, 'jobs/job_applications.html', {
        'job': job,
        'applications': applications,
        'applications': applications_page,
        'status_filter': status_filter
    })

@login_required
def update_application_status(request, application_id):
    application = get_object_or_404(Application, id=application_id, job__creator=request.user)  # Only HRs who posted the job

    if request.method == "POST":
        new_status = request.POST.get('status')
        if new_status in dict(Application.STATUS_CHOICES):
            application.status = new_status
            application.save()
            messages.success(request, "Application status updated successfully!")
        else:
            messages.error(request, "Invalid status selected.")
        return redirect('job_applications', job_id=application.job.id)

    return render(request, 'jobs/application_detail.html', {'application': application})
