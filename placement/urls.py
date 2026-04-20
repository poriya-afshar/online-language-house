from django.urls import path
from django.conf.urls.i18n import set_language
from . import views

urlpatterns = [
    path('placement-test/', views.placement_test, name='placement_test'),
    path('placement-test/questions/', views.get_questions, name='placement_questions'),
    path('placement-test/save/', views.save_placement_result, name='save_placement_result'),
    path('i18n/set-language/', set_language, name='set_language'),
]