from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import models
from .models import *
from placement.models import PlacementQuestion, PlacementTestSettings


# ==========================
# Home Page
# ==========================
def home(request):
    # ---------- Contact Form ----------
    if request.method == "POST" and "message" in request.POST:
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        if name and email and message:
            ContactMessage.objects.create(
                name=name,
                email=email,
                message=message
            )

            messages.success(request, "پیام شما با موفقیت ارسال شد.")
            return redirect("home")

    # ---------- Data For Template ----------
    context = {
        "about": About.objects.first(),
        "courses": Course.objects.filter(is_active=True),
        "teachers": Teacher.objects.filter(is_active=True),
        "testimonials": Testimonial.objects.filter(is_approved=True),
        "social_links": SocialLink.objects.all(),
        "hero": Hero.objects.first(),
        "stats": SiteStats.objects.first(),
    }

    return render(request, "core/index.html", context)


# ==========================
# Course Detail Page
# ==========================
def course_detail(request, id):
    course = get_object_or_404(Course, id=id, is_active=True)
    return render(request, "core/course_detail.html", {
        "course": course
    })


def course_placement_test(request, id):
    """Render placement test for a specific course.

    A button on the course detail page will link here. The same generic
    template is reused; JS will request questions filtered by course id.
    """
    course = get_object_or_404(Course, id=id, is_active=True)

    # at least one question linked to course (or global) with options?
    from django.db.models import Count
    has_q = PlacementQuestion.objects.filter(is_active=True).filter(
        models.Q(course=course) | models.Q(course__isnull=True)
    ).annotate(opts=Count('options')).filter(opts__gt=0).exists()

    settings_obj = PlacementTestSettings.objects.first()
    duration = settings_obj.total_duration_minutes if settings_obj else 10

    context = {
        "duration_seconds": duration * 60,
        "no_questions": not has_q,
        "course": course,
    }
    return render(request, "placement/placement_test.html", context)


# ==========================
# Placement Test
# ==========================
def placement_test(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        score = request.POST.get("score")
        level_result = request.POST.get("level_result")

        if name and email:
            PlacementTestSubmission.objects.create(
                name=name,
                email=email,
                score=score or 0,
                level_result=level_result or "Unknown"
            )

            messages.success(request, "نتیجه تست با موفقیت ثبت شد.")
            return redirect("placement_test")

    return render(request, "placement/placement_test.html")


def teacher_detail(request, id):
    teacher = get_object_or_404(Teacher, id=id, is_active=True)
    return render(request, "core/teacher_detail.html", {
        "teacher": teacher
    })


def enroll(request, id):
    course = get_object_or_404(Course, id=id, is_active=True)

    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")

        # فعلاً ساده
        messages.success(request, "درخواست ثبت‌نام شما ارسال شد.")
        return redirect("course_detail", id=course.id)

    return render(request, "core/enroll.html", {
        "course": course
    })
