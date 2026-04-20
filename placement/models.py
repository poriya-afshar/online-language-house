from django.db import models

LEVEL_CHOICES = [
    ('A1', 'A1 - Beginner'),
    ('A2', 'A2 - Elementary'),
    ('B1', 'B1 - Intermediate'),
    ('B2', 'B2 - Upper-Intermediate'),
    ('C1', 'C1 - Advanced'),
    ('C2', 'C2 - Mastery'),
]


class PlacementTestSettings(models.Model):
    """تنظیمات کلی تست تعیین سطح"""

    total_duration_minutes = models.PositiveIntegerField(
        default=10,
        verbose_name="مدت زمان کل آزمون (دقیقه)"
    )

    class Meta:
        verbose_name = "تنظیمات تست تعیین سطح"
        verbose_name_plural = "تنظیمات تست تعیین سطح"

    def __str__(self):
        return "تنظیمات تست تعیین سطح"


class PlacementQuestion(models.Model):
    """سوالات تست تعیین سطح — اضافه شده توسط استاد از پنل ادمین"""
    text = models.TextField(verbose_name='متن سوال')
    level = models.CharField(max_length=2, choices=LEVEL_CHOICES, verbose_name='سطح سوال')
    explanation = models.TextField(blank=True, verbose_name='توضیح پس از پاسخ')
    order = models.PositiveIntegerField(default=0, verbose_name='ترتیب نمایش')
    is_active = models.BooleanField(default=True, verbose_name='فعال')

    class Meta:
        ordering = ['order']
        verbose_name = 'سوال تعیین سطح'
        verbose_name_plural = 'سوالات تعیین سطح'

    def __str__(self):
        return f'[{self.level}] {self.text[:60]}'


class QuestionOption(models.Model):
    """گزینه‌های هر سوال"""
    question = models.ForeignKey(PlacementQuestion, on_delete=models.CASCADE,
                                 related_name='options', verbose_name='سوال')
    text = models.CharField(max_length=300, verbose_name='متن گزینه')
    is_correct = models.BooleanField(default=False, verbose_name='پاسخ صحیح')

    class Meta:
        verbose_name = 'گزینه'
        verbose_name_plural = 'گزینه‌ها'

    def __str__(self):
        return f'{"✓" if self.is_correct else "✗"} {self.text[:50]}'


class PlacementResult(models.Model):
    """نتایج تست دانشجویان"""
    name = models.CharField(max_length=150, verbose_name='نام دانش‌آموز')
    email = models.EmailField(blank=True, verbose_name='ایمیل')
    level = models.CharField(max_length=2, choices=LEVEL_CHOICES, verbose_name='سطح تشخیص داده شده')
    score = models.PositiveIntegerField(verbose_name='تعداد پاسخ صحیح')
    total = models.PositiveIntegerField(verbose_name='تعداد کل سوالات')
    time_seconds = models.PositiveIntegerField(default=0, verbose_name='مدت زمان (ثانیه)')
    taken_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ آزمون')

    class Meta:
        ordering = ['-taken_at']
        verbose_name = 'نتیجه تست'
        verbose_name_plural = 'نتایج تست‌ها'

    def __str__(self):
        return f'{self.name} — {self.level} ({self.score}/{self.total})'

    @property
    def percentage(self):
        return round((self.score / self.total) * 100) if self.total else 0
