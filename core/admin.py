from django.contrib import admin
from .models import *


class LearningOutcomeInline(admin.TabularInline):
    model = LearningOutcome
    extra = 1



@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "level", "duration", "test_level", "certificate")
    search_fields = ("title", "description", "test_level")
    list_filter = ("level", "certificate")
    inlines = [LearningOutcomeInline]
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'image', 'is_active')
        }),
        ('Metadata', {
            'fields': ('level', 'duration', 'test_level', 'test_duration', 'certificate', 'access')
        }),
    )


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ("name", "expertise")
    search_fields = ("name", "expertise")


@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    list_display = ("title",)


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("name", "role")
    search_fields = ("name",)


@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ("name", "url", "icon_class")
    search_fields = ("name",)

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "created_at")
    readonly_fields = ("name", "email", "message", "created_at")
    ordering = ("-created_at",)


@admin.register(PlacementTestSubmission)
class PlacementTestAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "score", "level_result", "created_at")
    readonly_fields = ("name", "email", "score", "level_result", "created_at")
    ordering = ("-created_at",)


admin.site.register(Hero)
admin.site.register(SiteStats)