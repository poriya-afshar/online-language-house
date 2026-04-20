# from django.contrib import admin
# from django.utils.html import format_html

# from .models import (
#     PlacementTestSettings,
#     PlacementQuestion,
#     QuestionOption,
#     PlacementResult
# )


# @admin.register(PlacementTestSettings)
# class PlacementTestSettingsAdmin(admin.ModelAdmin):
#     list_display = ("total_duration_minutes",)

#     def has_add_permission(self, request):
#         """
#         جلوگیری از ساخت چند تنظیم.
#         فقط یک رکورد مجاز است.
#         """
#         if PlacementTestSettings.objects.exists():
#             return False
#         return True


# class QuestionOptionInline(admin.TabularInline):
#     model = QuestionOption
#     extra = 4
#     min_num = 2
#     max_num = 6
#     fields = ("text", "is_correct")


# @admin.register(PlacementQuestion)
# class PlacementQuestionAdmin(admin.ModelAdmin):

#     list_display = (
#         "short_text",
#         "level",
#         "order",
#         "is_active",
#         "option_count"
#     )

#     list_filter = ("level", "is_active")
#     list_editable = ("order", "is_active")
#     search_fields = ("text",)
#     ordering = ("order",)
#     inlines = [QuestionOptionInline]

#     fieldsets = (
#         ("سوال", {
#             "fields": ("text", "level", "explanation")
#         }),
#         ("تنظیمات", {
#             "fields": ("order", "is_active"),
#             "classes": ("collapse",)
#         }),
#     )

#     def short_text(self, obj):
#         return obj.text[:70] + ("..." if len(obj.text) > 70 else "")

#     short_text.short_description = "متن سوال"

#     def option_count(self, obj):
#         total = obj.options.count()
#         correct = obj.options.filter(is_correct=True).count()

#         color = "green" if correct == 1 else "red"

#         return format_html(
#             "{} گزینه — <span style='color:{}; font-weight:bold'>{} صحیح</span>",
#             total,
#             color,
#             correct
#         )

#     option_count.short_description = "گزینه‌ها"


# @admin.register(PlacementResult)
# class PlacementResultAdmin(admin.ModelAdmin):

#     list_display = (
#         "name",
#         "email",
#         "level",
#         "score_display",
#         "percentage_display",
#         "time_display",
#         "taken_at"
#     )

#     list_filter = ("level", "taken_at")
#     search_fields = ("name", "email")
#     readonly_fields = (
#         "name",
#         "email",
#         "level",
#         "score",
#         "total",
#         "time_seconds",
#         "taken_at"
#     )
#     ordering = ("-taken_at",)

#     def score_display(self, obj):
#         return f"{obj.score} / {obj.total}"

#     score_display.short_description = "امتیاز"

#     def percentage_display(self, obj):

#         pct = obj.percentage

#         if pct >= 70:
#             color = "#2ab09a"
#         elif pct >= 40:
#             color = "#c9a84c"
#         else:
#             color = "#e05c5c"

#         return format_html(
#             "<span style='color:{}; font-weight:bold'>{}%</span>",
#             color,
#             pct
#         )

#     percentage_display.short_description = "درصد"

#     def time_display(self, obj):

#         minutes = obj.time_seconds // 60
#         seconds = obj.time_seconds % 60

#         return f"{minutes}:{seconds:02d}"

#     time_display.short_description = "مدت زمان"

#     def has_add_permission(self, request):
#         """
#         نتایج فقط توسط سیستم ثبت می‌شود.
#         """
#         return False



from django.contrib import admin
from django.utils.html import format_html

from .models import (
    PlacementTestSettings,
    PlacementQuestion,
    QuestionOption,
    PlacementResult
)


@admin.register(PlacementTestSettings)
class PlacementTestSettingsAdmin(admin.ModelAdmin):
    list_display = ("total_duration_minutes",)

    def has_add_permission(self, request):
        """
        جلوگیری از ساخت چند تنظیم.
        فقط یک رکورد مجاز است.
        """
        if PlacementTestSettings.objects.exists():
            return False
        return True


class QuestionOptionInline(admin.TabularInline):
    model = QuestionOption
    extra = 4
    min_num = 2
    max_num = 6
    fields = ("text", "is_correct")


@admin.register(PlacementQuestion)
class PlacementQuestionAdmin(admin.ModelAdmin):

    list_display = (
        "short_text",
        "level",
        "order",
        "is_active",
        "option_count"
    )

    list_filter = ("level", "is_active")
    list_editable = ("order", "is_active")
    search_fields = ("text",)
    ordering = ("order",)
    inlines = [QuestionOptionInline]

    fieldsets = (
        ("سوال", {
            "fields": ("text", "level", "explanation")
        }),
        ("تنظیمات", {
            "fields": ("order", "is_active"),
            "classes": ("collapse",)
        }),
    )

    def short_text(self, obj):
        return obj.text[:70] + ("..." if len(obj.text) > 70 else "")

    short_text.short_description = "متن سوال"

    def option_count(self, obj):
        total = obj.options.count()
        correct = obj.options.filter(is_correct=True).count()

        color = "green" if correct == 1 else "red"

        return format_html(
            "{} گزینه — <span style='color:{}; font-weight:bold'>{} صحیح</span>",
            total,
            color,
            correct
        )

    option_count.short_description = "گزینه‌ها"


@admin.register(PlacementResult)
class PlacementResultAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "phone",          # جایگزین email
        "level",
        "score_display",
        "percentage_display",
        "time_display",
        "taken_at"
    )

    list_filter = ("level", "taken_at")
    search_fields = ("name", "phone")   # جایگزین email
    readonly_fields = (
        "name",
        "phone",          # جایگزین email
        "level",
        "score",
        "total",
        "time_seconds",
        "taken_at"
    )
    ordering = ("-taken_at",)

    def score_display(self, obj):
        return f"{obj.score} / {obj.total}"

    score_display.short_description = "امتیاز"

    def percentage_display(self, obj):

        pct = obj.percentage

        if pct >= 70:
            color = "#2ab09a"
        elif pct >= 40:
            color = "#c9a84c"
        else:
            color = "#e05c5c"

        return format_html(
            "<span style='color:{}; font-weight:bold'>{}%</span>",
            color,
            pct
        )

    percentage_display.short_description = "درصد"

    def time_display(self, obj):

        minutes = obj.time_seconds // 60
        seconds = obj.time_seconds % 60

        return f"{minutes}:{seconds:02d}"

    time_display.short_description = "مدت زمان"

    def has_add_permission(self, request):
        """
        نتایج فقط توسط سیستم ثبت می‌شود.
        """
        return False