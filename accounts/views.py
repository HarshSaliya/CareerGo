from django.shortcuts import render,redirect
from django.contrib import messages, auth
from accounts.models import User ,Subscriber
from applications.models import Application 

from django.contrib.auth.decorators import login_required

# Create your views here.
def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email,password=password)

        if user is not None: # Check if the user is found in db
            auth.login(request,user)
            messages.success(request,"You are now logged in!")
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid credentials")
            return redirect('login')
    else:
        return render(request,'accounts/login.html')

def register(request):
    if request.method == 'POST':
       # Get form values
       first_name = request.POST['first_name']
       last_name = request.POST['last_name']
       email = request.POST['email']
       password = request.POST['password']
       confirm_password  = request.POST['confirm_password']
       role = request.POST.get('role', 'job_seeker')

       # Check if passwords match
       if password == confirm_password:
                # Check if the email in db is equal to the input email 
               if User.objects.filter(email=email).exists():
                   messages.error(request, 'That email is already being used!')
                   return redirect('register') 
               else:
                   # Register the user
                   user = User.objects.create_user(password=password,
                                                   email=email,
                                                   first_name=first_name,
                                                   last_name=last_name,
                                                   role=role) # type: ignore
                   user.save()
                   messages.success(request,'You are now registered and can log in')
                   return redirect('login')
                   

       else:
           messages.error(request , 'Passwords do not match!')
           return redirect('register')
    else:
        return render(request,'accounts/register.html')
        
def logout(request):
    if request.method == "POST":
        auth.logout(request)
        messages.success(request,"You are now logged out")
        return redirect('index')

@login_required()
def dashboard(request):
    # user_applications = Application.objects.order_by('-created_at').filter(applicant=request.user)
    user_applications = Application.objects.filter(applicant=request.user).select_related('job').order_by('-created_at')
    
    context = {
        'applications': user_applications
    }
    return render(request,'accounts/dashboard.html', context)

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import PersonalInfo, EducationInfo, JobInfo

@login_required
def user_profile(request):
    user = request.user
    personal_info, _ = PersonalInfo.objects.get_or_create(user=user)
    education_info, _ = EducationInfo.objects.get_or_create(user=user)
    job_info, _ = JobInfo.objects.get_or_create(user=user)

    if request.method == 'POST':
        # Update Personal Info
        if 'update_personal' in request.POST:
            personal_info.phone = request.POST.get('phone')
            personal_info.address = request.POST.get('address')
            personal_info.city = request.POST.get('city')
            personal_info.state = request.POST.get('state')
            personal_info.country = request.POST.get('country')
            if request.FILES.get('profile_image'):
                personal_info.profile_image = request.FILES['profile_image']
            personal_info.save()
            messages.success(request, 'Personal information updated successfully!')
        
        # Update Education Info
        elif 'update_education' in request.POST:
            education_info.highest_degree = request.POST.get('highest_degree')
            education_info.university_name = request.POST.get('university_name')
            education_info.passing_year = request.POST.get('passing_year')
            education_info.grade = request.POST.get('grade')
            education_info.save()
            messages.success(request, 'Education information updated successfully!')
        
        # Update Job Info
        elif 'update_job' in request.POST:
            job_info.current_position = request.POST.get('current_position')
            job_info.company_name = request.POST.get('company_name')
            job_info.years_of_experience = request.POST.get('years_of_experience')
            job_info.skills = request.POST.get('skills')
            if request.FILES.get('resume'):
                job_info.resume = request.FILES['resume']
            job_info.save()
            messages.success(request, 'Job information updated successfully!')
        
        return redirect('user_profile')
    
    context = {
        'user': user,
        'personal_info': personal_info,
        'education_info': education_info,
        'job_info': job_info,
    }
    return render(request, 'accounts/user_profile.html', context)



def subscribe(request):
    if request.method == "POST":
        email = request.POST.get("email")
        
        # Check if email already exists
        if Subscriber.objects.filter(email=email).exists():
            messages.error(request, "This email is already subscribed.")
        else:
            Subscriber.objects.create(email=email)
            messages.success(request, "You have successfully subscribed!")

    return render(request, "index.html")



def subscribe(request):
    if request.method == "POST":
        email = request.POST.get("email")

        if Subscriber.objects.filter(email=email).exists():
            messages.error(request, "You are already subscribed!")
        else:
            Subscriber.objects.create(email=email)
            messages.success(request, "Subscription successful!")

        return redirect("index")  # Redirects back to homepage

    return redirect("index") 



# from django.shortcuts import render
# from django.contrib import messages

# def forgot_password_view(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         # Later we'll add logic to send email
#         messages.success(request, 'If this email exists, a reset link will be sent.')
#         return render(request, 'forgot_password.html')
    
#     return render(request, 'accounts/forgot_password.html')

from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model
from .utils import account_activation_token


User = get_user_model()

def forgot_password_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)

            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = account_activation_token.make_token(user)
            # reset_link = request.build_absolute_uri(f'/reset-password/{uid}/{token}/')
            reset_link = request.build_absolute_uri(f'/accounts/reset-password/{uid}/{token}/')


            subject = 'Reset Your Password'
            html_message = render_to_string('accounts/reset_password_email.html', {
                'user': user,
                'reset_link': reset_link
            })

            send_mail(subject, '', 'youremail@gmail.com', [email], html_message=html_message)
            messages.success(request, 'Password reset link has been sent to your email.')

        except User.DoesNotExist:
            messages.error(request, 'This email is not registered.')
            
    return render(request, 'accounts/forgot_password.html')



from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from .utils import account_activation_token
from django.http import HttpResponse


User = get_user_model()

def reset_password_view(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        if request.method == 'POST':
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')

            if password == confirm_password:
                user.password = make_password(password)
                user.save()
                messages.success(request, "Password reset successful. You can now log in.")
                return redirect('login')
            else:
                messages.error(request, "Passwords do not match.")

        return render(request, 'accounts/reset_password_form.html')
    else:
        return HttpResponse('Invalid or expired link')
