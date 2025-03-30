from django.urls import path

from .import views

urlpatterns = [
    path('' ,  views.index , name = 'jobs') ,
    path('<int:job_id>' , views.job , name = 'job') ,
    path('search' , views.search , name = 'search') ,
    path('applyjob<int:job_id>', views.applyjob, name='applyjob_with_job_id'),
    path('post-job/', views.post_job, name='post_job'),
    path('manage/', views.manage_jobs, name='manage_jobs'),
    path('<int:job_id>/applications/', views.job_applications, name='job_applications'),
    path('edit/<int:job_id>/', views.edit_job, name='edit_job'),
    path('delete/<int:job_id>/', views.delete_job, name='delete_job'),
    path('application/<int:application_id>/update/', views.job_applications, name='update_application_status'),
     path('jobs/application/<int:application_id>/update/', views.update_application_status, name='update_application_status'),
    
]