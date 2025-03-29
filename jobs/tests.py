# viewws.py : from django.contrib.auth.decorators import login_required
# from django.shortcuts import render
# from jobs.models import Job
# from applications.models import Application
# @login_required
# def company_dashboard(request):
#     # Ensure only company users can access
#     if request.user.role != 'company':
#         messages.error(request, 'Access denied. Company accounts only.')
#         return redirect('dashboard')
#     # Get jobs created by the logged-in company
#     jobs = Job.objects.filter(creator=request.user).annotate(
#         application_count=Count('application')
#     )
#     # Get recent applications for jobs created by this company
#     recent_applications = Application.objects.filter(
#         creator_id=request.user.id
#     ).order_by('-contact_date')[:10]
#     context = {
#         'jobs': jobs,
#         'recent_applications': recent_applications
#     }
#     return render(request, 'accounts/company_dashboard.html', context)
# @login_required
# def job_applications(request, job_id):
#     # Get detailed applications for a specific job
#     job = get_object_or_404(Job, id=job_id, creator=request.user)
#     applications = Application.objects.filter(job_id=job_id)
    
#     context = {
#         'job': job,
#         'applications': applications
#     }
#     return render(request, 'accounts/job_applications.html', context)
# @login_required
# def update_application_status(request, application_id):
#     if request.method == 'POST':
#         application = get_object_or_404(Application, id=application_id)
        
#         # Ensure only the job creator can update status
#         if application.creator_id != request.user.id:
#             return JsonResponse({'error': 'Unauthorized'}, status=403)
        
#         new_status = request.POST.get('status')
#         application.status = new_status
#         application.save()
        
#         return JsonResponse({'success': True}) , urls.py:urlpatterns = [
#     # ... existing patterns
#     path('company-dashboard/', views.company_dashboard, name='company_dashboard'),
#     path('job-applications//', views.job_applications, name='job_applications'),
#     path('update-application-status//', views.update_application_status, name='update_application_status'),
# ]