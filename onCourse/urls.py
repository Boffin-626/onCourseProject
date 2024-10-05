# urls.py
from django.urls import path
from . import views

app_name = 'onCourse'
urlpatterns = [
    path('', views.index, name='index'),

    path('add_learner_info/', views.add_learner_info, name='add_learner_info'),
    path('upload-report/', views.upload_report, name='upload_report'),
    path('report_uploaded', views.report_uploaded, name='report_uploaded'),
    # Edit Learner Info
    # Update Learner Info
    path('learner_info_list/', views.learner_info_list, name='learner_info_list'),
    path('learner_dashboard/', views.learner_dashboard, name='learner_dashboard'),
    path('learner_detail/', views.learner_detail, name='learner_detail'),
    path('view_learner_progress/', views.view_learner_progress, name='view_learner_progress'),
    path('load_concepts/', views.load_concepts, name='load_concepts'),
    path('concept_quiz/', views.concept_quiz, name='concept_quiz'),
    path('my_rewards/', views.my_rewards, name='my_rewards'),
    path('achievements/', views.achievements, name='achievements'),
    path('learning_materials', views.learning_materials, name='learning_materials'), 
    path('calendar/', views.calendar, name='calendar'),   
    path('learner_progress_form/', views.learner_progress_form, name='learner_progress_form'),
    path('learner_progress_detail/', views.learner_progress_detail, name='learner_progress_detail'),
    path('load_questions/', views.load_questions, name='load_questions'),
    path('learner_progress_list/', views.learner_progress_list, name='learner_progress_list'),
    path('report_update/', views.report_update, name='report_update'),
    path('submit_answers/', views.submit_answers, name='submit_answers'),
    path('learner_grade/', views.learner_grade, name='learner_grade'),
    path('concept_list/,', views.concept_list, name='concept_list'),
    path('concept_detail/', views.concept_detail, name='concept_detail'),
    
    path('ussd_request/', views.ussd_request, name='ussd_request'),
    path('whatsapp_request/', views.whatsapp_request, name='whatsapp_request'),
    
    path('parent_dashboard/', views.parent_dashboard, name='parent_dashboard'),
    path('parent_views/', views.parent_views, name='parent_views'),
    #path('parent_analytics/', views.parent_analytics, name='parent_analytics'),
    
    path('teacher_dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('teacher_views/', views.teacher_views, name='teacher_views'),
    
    path('hod_dashboard/', views.hod_dashboard, name='hod_dashboard'),
    path('hod_views/', views.hod_views, name='hod_views'),
    path('HOD_Correspondence/', views.HOD_Correspondence, name='HOD_Correspondence'),
    
    path('district_dashboard/', views.district_dashboard, name='district_dashboard'),
    path('district_views/', views.district_views, name='district_views'),

    #path('comparative_analytics/', views.comparative_analytics, name='comparative_analytics'),
    #path('all_learners_analytics/', views.all_learners_analytics, name='all_learners_analytics'),
]

