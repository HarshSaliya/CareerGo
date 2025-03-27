from django.shortcuts import render
from django.http import JsonResponse
from .forms import ResumeUploadForm
from .models import Resume
from .utils import extract_text_from_resume, analyze_resume

def home(request):
    form = ResumeUploadForm()
    return render(request, "home.html", {"form": form})

def process_resume(request):
    if request.method == "POST" and request.FILES.get("resume_file"):
        form = ResumeUploadForm(request.POST, request.FILES)
        if form.is_valid():
            resume_instance = form.save()

            # Extract text from resume
            text, error = extract_text_from_resume(resume_instance.resume_file)
            if error:
                return JsonResponse({"score": 0, "feedback": error})

            # Analyze resume
            score, feedback = analyze_resume(
                text, 
                resume_instance.profession,  # Profession field from form
                resume_instance.experience_level  # Experience level field from form
            )
            resume_instance.score = score
            resume_instance.feedback = feedback
            resume_instance.save()

            return JsonResponse({"score": score, "feedback": feedback})

    return JsonResponse({"error": "Invalid request"}, status=400)
