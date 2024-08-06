# urls.py
from django.urls import path
from . import views

app_name = 'onCourse'
urlpatterns = [
    path('', views.index, name='index'),
    path('learner_progress', views.learner_progress, name='learner_progress'),
    path('learner_progress_success/', views.learner_progress_success, name='learner_progress_success'),
    path('learner_analytics/', views.learner_analytics, name='learner_analytics'),
    path('comparative_analytics/', views.comparative_analytics, name='comparative_analytics'),
    path('all_learners_analytics/', views.all_learners_analytics, name='all_learners_analytics'),
    path('ussd_request/', views.ussd_request, name='ussd_request'),
    path('whatsapp_request/', views.whatsapp_request, name='whatsapp_request'),
]