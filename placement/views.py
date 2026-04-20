import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db import models
from .models import PlacementQuestion, PlacementResult, PlacementTestSettings


def placement_test(request):
    """نمایش صفحهٔ آزمون (بدون ارسال سوال‌ها به‌صورت ساکن)."""

    # just check whether at least one active question with at least one option
    # exists so that we can disable the button or show a warning. the real list
    # is fetched later via AJAX.
    from django.db.models import Count
    has_questions = PlacementQuestion.objects.filter(is_active=True)
    # only count questions that actually have options defined
    has_questions = has_questions.annotate(opts=Count('options')).filter(opts__gt=0).exists()

    settings_obj = PlacementTestSettings.objects.first()
    duration = settings_obj.total_duration_minutes if settings_obj else 10

    context = {
        # JSON payload removed from template, questions will be loaded with JS
        "duration_seconds": duration * 60,
        "no_questions": not has_questions,
    }
    return render(request, "placement/placement_test.html", context)


def get_questions(request):
    """AJAX endpoint returning all active questions/options as JSON."""
    qs = PlacementQuestion.objects.filter(is_active=True)
    # exclude questions that don't yet have any options defined
    from django.db.models import Count
    qs = qs.annotate(opts=Count('options')).filter(opts__gt=0)
    qs = qs.prefetch_related("options")

    questions_data = []
    for q in qs:
        questions_data.append({
            "id": q.id,
            "text": q.text,
            "options": [{"text": opt.text, "is_correct": opt.is_correct} for opt in q.options.all()]
        })

    settings_obj = PlacementTestSettings.objects.first()
    duration = settings_obj.total_duration_minutes * 60 if settings_obj else 600

    return JsonResponse({
        "questions": questions_data,
        "duration_seconds": duration,
    })


@require_POST
def save_placement_result(request):
    try:
        data = json.loads(request.body)
        PlacementResult.objects.create(
            name=data.get("name", "Unknown"),
            level=data.get("level", "A1"),
            score=int(data.get("score", 0)),
            total=int(data.get("total", 0)),
            time_seconds=int(data.get("time_seconds", 0))
        )
        return JsonResponse({"status": "success"})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=400)
