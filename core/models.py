from django.db import models


class Course(models.Model):
    title = models.CharField("عنوان دوره", max_length=200)
    level = models.CharField("سطح دوره", max_length=100)
    duration = models.CharField("مدت زمان", max_length=100)
    description = models.TextField("توضیحات")
    image = models.ImageField("تصویر", upload_to='courses/', blank=True, null=True)
    # ------------------------------------
    # additional metadata requested by client
    test_level = models.CharField("سطح تست دوره", max_length=100, blank=True, help_text="مثلاً A1/A2 یا آسان/متوسط")
    test_duration = models.CharField("مدت زمان آزمون", max_length=100, blank=True, help_text="مثلاً 10 ساعت")
    certificate = models.BooleanField("گواهینامه دارد", default=True)
    access = models.CharField("دسترسی", max_length=200, default="موبایل + دسکتاپ")
    # ------------------------------------
    is_active = models.BooleanField("فعال باشد", default=True)

    class Meta:
        verbose_name = "دوره"
        verbose_name_plural = "دوره‌ها"

    def __str__(self):
        return self.title


class Teacher(models.Model):
    name = models.CharField("نام استاد", max_length=200)
    # optional language field which templates already reference
    language = models.CharField("زبان تدریس", max_length=100, blank=True)
    expertise = models.CharField("تخصص", max_length=200)
    experience_years = models.IntegerField("سال تجربه")
    bio = models.TextField("رزومه")
    image = models.ImageField("تصویر", upload_to='teachers/', blank=True, null=True)
    is_active = models.BooleanField("فعال باشد", default=True)

    class Meta:
        verbose_name = "استاد"
        verbose_name_plural = "اساتید"

    def __str__(self):
        return self.name


class About(models.Model):
    title = models.CharField("عنوان", max_length=200)
    description = models.TextField("توضیحات")
    image = models.ImageField("تصویر", upload_to='about/', blank=True, null=True)
    founded_year = models.CharField("سال تأسیس", max_length=50)

    class Meta:
        verbose_name = "درباره"
        verbose_name_plural = "بخش درباره"

    def __str__(self):
        return "About"


# class Testimonial(models.Model):
#     name = models.CharField("نام", max_length=200)
#     role = models.CharField("نقش", max_length=200)
#     text = models.TextField("متن نظر")
#     image = models.ImageField("تصویر", upload_to='testimonials/', blank=True, null=True)
#     is_approved = models.BooleanField("تأیید شده", default=False)

#     class Meta:
#         verbose_name = "نظر دانش‌آموز"
#         verbose_name_plural = "نظرات دانش‌آموزان"

#     def __str__(self):
#         return self.name


class SocialLink(models.Model):
    name = models.CharField("نام شبکه", max_length=100)
    icon_class = models.CharField("کلاس آیکن", max_length=100)
    url = models.URLField("لینک")

    class Meta:
        verbose_name = "شبکه اجتماعی"
        verbose_name_plural = "شبکه‌های اجتماعی"

    def __str__(self):
        return self.name


class ContactMessage(models.Model):
    name = models.CharField("نام", max_length=200)
    email = models.EmailField("ایمیل")
    message = models.TextField("پیام")
    created_at = models.DateTimeField("تاریخ ارسال", auto_now_add=True)
    is_read = models.BooleanField("خوانده شده", default=False)
    phone = models.CharField("شماره تلفن", max_length=20, blank=False, null=False, default='')

    class Meta:
        verbose_name = "پیام تماس"
        verbose_name_plural = "پیام‌های تماس"

    def __str__(self):
        return self.name


class Hero(models.Model):
    title_line1 = models.CharField("خط اول عنوان", max_length=200, blank=True, null=True)
    title_highlight = models.CharField("متن برجسته", max_length=200, blank=True, null=True)
    subtitle = models.TextField("زیرعنوان", blank=True, null=True)
    background_image = models.ImageField("تصویر پس‌زمینه", upload_to='hero/', blank=True, null=True)

    class Meta:
        verbose_name = "بخش هدر"
        verbose_name_plural = "بخش هدر سایت"

    def __str__(self):
        return "Hero"




class LearningOutcome(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='learning_outcomes', verbose_name='دوره')
    text = models.CharField("خروجی یادگیری", max_length=300)

    class Meta:
        verbose_name = 'خروجی یادگیری'
        verbose_name_plural = 'خروجی‌های یادگیری'

    def __str__(self):
        return self.text[:50]


class SiteStats(models.Model):
    students = models.CharField("دانش‌آموزان", max_length=50, blank=True, null=True)
    courses = models.CharField("دوره‌ها", max_length=50, blank=True, null=True)
    teachers = models.CharField("اساتید", max_length=50, blank=True, null=True)
    satisfaction = models.CharField("رضایت", max_length=50, blank=True, null=True)

    class Meta:
        verbose_name = "آمار سایت"
        verbose_name_plural = "آمار سایت"

    def __str__(self):
        return "Stats"
