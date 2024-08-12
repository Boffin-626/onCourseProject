# urls.py
from django.urls import path
from . import views

app_name = 'onCourse'
urlpatterns = [
    path('', views.index, name='index'),
    path('learner_progress_form/<int:learner_id>/', views.learner_progress_form, name='learner_progress_form'),
    path('learner_progress_detail/<int:learner_id>/', views.learner_progress_detail, name='learner_progress_detail'),
    path('learner_progress_list/', views.learner_progress_list, name='learner_progress_list'),
    path('report_update/', views.report_update, name='report_update'),
    path('ussd_request/', views.ussd_request, name='ussd_request'),
    path('whatsapp_request/', views.whatsapp_request, name='whatsapp_request'),
    path('parent_dashboard/', views.parent_dashboard, name='parent_dashboard'),
    path('view_learner_progress/', views.view_learner_progress, name='view_learner_progress'),
    path('teacher_dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('learner_detail/', views.learner_detail, name='learner_detail'),
    path('hod_dashboard/', views.hod_dashboard, name='hod_dashboard'),
    path('district_dashboard/', views.district_dashboard, name='district_dashboard'),

    #path('comparative_analytics/', views.comparative_analytics, name='comparative_analytics'),
    #path('all_learners_analytics/', views.all_learners_analytics, name='all_learners_analytics'),
]

