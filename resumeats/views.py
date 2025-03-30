from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Resume
from .utils import extract_text_from_resume, analyze_resume
import os

@login_required
def home(request):
    return render(request, "home.html")

@login_required
def process_resume(request):
    if request.method == "POST":
        profession = request.POST.get("profession")
        experience_level = request.POST.get("experience_level")
        resume_file = request.FILES.get("resume_file")

        # Validate required fields
        if not all([profession, experience_level, resume_file]):
            return JsonResponse({"error": "All fields are required."}, status=400)

        # Validate file type (Only PDF and DOCX allowed)
        allowed_extensions = [".pdf", ".docx"]
        file_extension = os.path.splitext(resume_file.name)[1].lower()
        if file_extension not in allowed_extensions:
            return JsonResponse({"error": "Only PDF and DOCX files are allowed."}, status=400)

        # Save resume instance
        resume_instance = Resume.objects.create(
            user=request.user,
            profession=profession,
            experience_level=experience_level,
            resume_file=resume_file
        )

        # Extract text from resume
        text, error = extract_text_from_resume(resume_instance.resume_file)
        if error:
            return JsonResponse({"score": 0, "feedback": error})

        # Analyze resume
        score, feedback = analyze_resume(text, profession, experience_level)
        resume_instance.score = score
        resume_instance.feedback = feedback
        resume_instance.save()

        return JsonResponse({"score": score, "feedback": feedback})

    return JsonResponse({"error": "Invalid request"}, status=400)
