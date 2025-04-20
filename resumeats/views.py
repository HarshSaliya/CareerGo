from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Resume
from .utils import extract_text_from_resume, analyze_resume
import os
import uuid
from decimal import Decimal
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Plan, Payment, DummyCreditCard ,Resume
from django.utils.timezone import now
from datetime import timedelta


@login_required
def home(request):
    return render(request, "home.html")

@login_required
def process_resume(request):
    if request.method == "POST":
        user = request.user

        # Fetch the latest successful payment
        latest_payment = Payment.objects.filter(user=user, status="success").order_by('-created_at').first()

        # Determine if the user has an active plan
        has_active_plan = False
        if latest_payment:
            plan_name = latest_payment.plan.name  # Get the plan name (e.g., '6_months')
            plan_duration = {
                "3_months": 90,
                "6_months": 180,
                "1_year": 365,
            }.get(plan_name, 0)

            # Check if the plan is still valid
            if latest_payment.created_at >= now() - timedelta(days=plan_duration):
                has_active_plan = True

        # ✅ FIX: Only restrict free users, allow paid users to continue  
        resume_count = Resume.objects.filter(user=request.user).count()
        if resume_count >= 3 and not has_active_plan:
            return JsonResponse({"error": "You have reached your free limit of 3 resume checks. Please buy a plan to continue."}, status=403)
        
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





def plan_list(request):
    """ Display available plans """
    plans = Plan.objects.all()
    return render(request, 'plans.html', {'plans': plans})

@login_required
def payment_page(request, plan_id):
    """ Show the payment form for the selected plan """
    plan = get_object_or_404(Plan, id=plan_id)
    gst = Decimal(plan.price) * Decimal(0.18)  # 18% GST
    total_amount = Decimal(plan.price) + gst

    return render(request, 'payment.html', {
        'plan': plan,
        'gst': gst,
        'total_amount': total_amount
    })

@login_required
def process_payment(request):
    """ Process the payment using dummy card details """
    if request.method == "POST":
        plan_id = request.POST.get("plan_id")
        card_number = request.POST.get("card_number")
        card_holder = request.POST.get("card_holder")
        expiry_date = request.POST.get("expiry_date")
        cvv = request.POST.get("cvv")

        # Fetch the plan
        plan = get_object_or_404(Plan, id=plan_id)
        gst = Decimal(plan.price) * Decimal(0.18)
        total_amount = Decimal(plan.price) + gst
        
        gst = gst.quantize(Decimal('0.01'))
        total_amount = total_amount.quantize(Decimal('0.01'))

        # Validate the card
        try:
            card = DummyCreditCard.objects.get(card_number=card_number, card_holder=card_holder, expiry_date=expiry_date, cvv=cvv)
        except DummyCreditCard.DoesNotExist:
            return JsonResponse({"status": "failed", "message": "Invalid card details"}, status=400)

        # Check balance
        if card.balance < total_amount:
            return JsonResponse({"status": "failed", "message": "Insufficient balance"}, status=400)

        # Deduct the amount
        card.balance -= total_amount
        card.save()

        # Create a payment record
        payment = Payment.objects.create(
            user=request.user,
            plan=plan,
            base_price=plan.price,
            gst=gst,
            total_amount=total_amount,
            status="success",
            transaction_id=str(uuid.uuid4())  # Unique transaction ID
        )

        return JsonResponse({"status": "success", "transaction_id": payment.transaction_id, "message": "Payment successful"})

    return JsonResponse({"status": "failed", "message": "Invalid request"}, status=400)
    