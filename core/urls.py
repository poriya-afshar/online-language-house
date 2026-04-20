from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path("courses/<int:id>/", views.course_detail, name="course_detail"),
    path("courses/<int:id>/enroll/", views.enroll, name="enroll"),

    path("teachers/<int:id>/", views.teacher_detail, name="teacher_detail"),

]