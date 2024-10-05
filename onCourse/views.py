# views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *

from django.db.models import Sum, Count, Q, Avg
from django.shortcuts import render
from datetime import datetime

from django.http import HttpResponse, JsonResponse
from django.utils.dateparse import parse_date

from django.contrib.auth import get_user_model
from django.db.models import Avg

from django.views.decorators.csrf import csrf_exempt
import africastalking
from twilio.twiml.messaging_response import MessagingResponse

from django.conf import settings

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import joblib
import pandas as pd
import numpy as np

from .image_processor import extract_text_from_image, parse_report_data, save_report_data

User = get_user_model()

def index(request):
    user = request.user
    context = {
        'is_learner': user.groups.filter(name='Learner').exists(),
        'is_parent': user.groups.filter(name='Parent').exists(),
        'is_teacher': user.groups.filter(name='Teacher').exists(),
        'is_hod': user.groups.filter(name='HOD').exists(),
        'is_district': user.groups.filter(name='District').exists(),
    }
    return render(request, 'onCourse/index.html', context)

def add_learner_info(request):
    if request.method == 'POST':
        form = LearnerInfoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('onCourse:learner_info_list')  # Redirect to the list of learners after submission
    else:
        form = LearnerInfoForm()
    context = {'form': form}
    return render(request, 'onCourse/add_learner_info.html', context)

def learner_info_list(request):
    learners = LearnerInfo.objects.all()
    context = {'learners': learners}
    return render(request, 'onCourse/learner_info_list.html', context)

def learner_dashboard(request):
    return render(request, 'onCourse/learner_dashboard.html')

def my_rewards(request):
    pass

def achievements(request):
    pass

def learning_materials(request):
    pass

def calendar(request):
    events = SchoolEvent.objects.all()  # Fetch all events
    context = {
        'events': events,  # Pass the events to the template
    }
    return render(request, 'onCourse/calendar.html', context)

def learner_progress_form(request):
    if request.method == 'POST':
        form = LearnerProgressForm(request.POST)
        if form.is_valid():
            learner_progress = form.save(commit=False)
            learner_progress.learner = request.user.learner  # Assuming learner is related to User
            learner_progress.save()
            return redirect('onCourse:learner_dashboard')  # Redirect to learner dashboard after saving
    else:
        form = LearnerProgressForm()

    context = {
        'form': form,
    }
    return render(request, 'onCourse/learner_progress_form.html', context)

def upload_report(request):
    # Assuming report_data is extracted correctly from the request
    report_data = extract_data_from_request(request)  # Placeholder for your extraction logic
    result = save_report_data(report_data)

    if result['learner']:
        # If learner is identified, we can access the learner's name
        return HttpResponse(f"Learner Grade for {result['learner'].name} saved successfully.")
    else:
        # Handle unidentified learner case
        if result['status'] == 'unidentified':
            return HttpResponse(f"Unidentified learner's report saved with grade: {result['grade']}.")
        elif result['status'] == 'not found':
            return HttpResponse(f"Report processed but learner '{report_data.get('learner_name')}' not found.")

def report_uploaded(request):
    return render(request, 'onCouse/report_uploaded.html')

def load_concepts(request):
    subject_id = request.GET.get('subject')
    concepts = Concept.objects.filter(subject_id=subject_id).order_by('name')
    return JsonResponse(list(concepts.values('id', 'name')), safe=False)

def concept_quiz(request, concept_id):
    concept = get_object_or_404(Concept, id=concept_id)
    questions = Question.objects.filter(concept=concept)[:2]

    if request.method == 'POST':
        total_score = 0
        for question in questions:
            selected_answer_id = request.POST.get(f'question-{question.id}')
            selected_answer = get_object_or_404(Answer, id=selected_answer_id)
            if selected_answer.is_correct:
                total_score += 1

        grasp_level = 'low' if total_score == 0 else 'medium' if total_score == 1 else 'high'
        LearnerProgress.objects.create(learner=request.user, concept=concept, grasp_level=grasp_level, score=total_score)

        return redirect('onCourse:learner_dashboard')
    context = {'concept': concept, 'questions': questions}
    return render(request, 'onCourse/concept_quiz.html', context)

def load_questions(request):
    concept_id = request.GET.get('concept')
    questions = Question.objects.filter(concept_id=concept_id)
    return render(request, 'onCourse/load_questions.html', {'questions': questions})

def learner_progress_detail(request):
    learner = get_object_or_404(Learner)
    progress = LearnerProgress.objects.filter(learner=learner)
    context = {
        'learner': learner, 
        'progress': progress
    } 
    return render(request, 'onCourse/learner_progress_detail.html', context)

def learner_progress_list(request):
    learners = Learner.objects.all()
    context = {'learners': learners}
    return render(request, 'onCourse/learner_progress_list.html', context)

def get_concepts(request, subject_id):
    concepts = Concept.objects.filter(subject_id=subject_id).values('id', 'name')
    return JsonResponse(list(concepts), safe=False)

def report_update(request):
    return render(request, 'onCourse/report_update.html')

def teacher_dashboard(request):
    return render(request, 'onCourse/teacher_dashboard.html')

def teacher_views(request):
    teacher = get_object_or_404(Teacher)
    
    # Fetch learners associated with this teacher
    learners = teacher.learners.all()
    
    # Filter LearnerProgress records associated with the learners
    learner_progress = LearnerProgress.objects.filter(learner__in=learners).select_related('learner', 'subject', 'concept')

    # Apply filters based on GET parameters
    if request.GET.get('subject'):
        learner_progress = learner_progress.filter(subject__name=request.GET.get('subject'))
    
    if request.GET.get('grasp_level'):
        learner_progress = learner_progress.filter(grasp_level=request.GET.get('grasp_level'))
    
    # Get distinct subjects for the dropdown
    subjects = teacher.subjects.all()

    context = {
        'teacher': teacher,
        'learner_progress': learner_progress,
        'learners': learners,
        'subjects': subjects,
    }
    return render(request, 'onCourse/teacher_views.html', context)

def learner_detail(request):
    learner = get_object_or_404(Learner)
    progress_reports = LearnerProgress.objects.filter(learner=learner).order_by('-created_at')
    
    if request.method == 'POST':
        form = TeacherCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            teacher = get_object_or_404(Teacher, user=request.user)  # Fetch the Teacher instance
            comment.teacher = teacher
            comment.progress_report_id = request.POST.get('progress_report_id')
            comment.save()
            return redirect('onCourse:learner_detail')
    else:
        form = TeacherCommentForm()

    context = {
        'learner': learner,
        'progress_reports': progress_reports,
        'form': form,
    }
    return render(request, 'onCourse/learner_detail.html', context)

def parent_dashboard(request):
    return render(request, 'onCourse/parent_dashboard.html')

def parent_views(request):
    parent = get_object_or_404(Parent)
    # Fetch learners associated with this parent
    learners = parent.learners.all()
    
    # Filter LearnerProgress records associated with the learners
    learner_progress = LearnerProgress.objects.filter(learner__in=learners).select_related('learner', 'subject', 'concept')

    # Optionally, you can add filters for subjects, date ranges, etc.
    if request.GET.get('subject'):
        learner_progress = learner_progress.filter(subject__name=request.GET.get('subject'))
    
    if request.GET.get('grasp_level'):
        learner_progress = learner_progress.filter(grasp_level=request.GET.get('grasp_level'))
    context = {
        'parent': parent,
        'learner_progress': learner_progress,
        'learners': learners,
    }
    return render(request, 'onCourse/parent_views.html', context)

def view_learner_progress(request):
    parent = get_object_or_404(Parent)
    learner = get_object_or_404(Learner)
    progress_reports = LearnerProgress.objects.filter(learner=learner).order_by('-created_at')

    context = {
        'parent': parent,
        'learner': learner,
        'progress_reports': progress_reports,
    }
    return render(request, 'onCourse/view_learner_progress.html', context)

def ussd_request(request):
    parent = get_object_or_404(Parent)
    if request.method == 'POST':
        form = USSDRequestForm(request.POST)
        if form.is_valid():
            ussd_request = form.save(commit=False)
            ussd_request.parent = parent
            ussd_request.save()
            # Add logic to send USSD response
            return redirect('onCourse:parent_dashboard', parent_id=parent.id)
    else:
        form = USSDRequestForm()
    context = {'parent': parent, 'form': form}
    return render(request, 'onCourse/ussd_request.html', context)

def whatsapp_request(request, parent_id):
    parent = get_object_or_404(Parent, id=parent_id)
    if request.method == 'POST':
        form = WhatsAppRequestForm(request.POST)
        if form.is_valid():
            whatsapp_request = form.save(commit=False)
            whatsapp_request.parent = parent
            whatsapp_request.save()
            # Add logic to send WhatsApp response
            return redirect('onCourse:parent_dashboard', parent_id=parent.id)
    else:
        form = WhatsAppRequestForm()
    context = {'parent': parent, 'form': form}
    return render(request, 'onCourse/whatsapp_request.html', context)

def hod_dashboard(request):
    return render(request, 'onCourse/hod_dashboard.html')

def hod_views(request):
    # Existing context setup
    total_learners = LearnerProgress.objects.values('learner').distinct().count()
    total_grasp_levels = LearnerProgress.objects.aggregate(avg_grasp_level=Avg('grasp_level'))
    reports_submitted = LearnerProgress.objects.count()
    
    subjects = Subject.objects.all()
    learner_progress = LearnerProgress.objects.select_related('learner', 'subject', 'concept').all()

    underperforming_learners = learner_progress.filter(grasp_level='low').count()

    # Handle message form submission
    if request.method == 'POST':
        form = HODMessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.hod = User.objects.get()  # Resolving SimpleLazyObject issue
            message.save()
            return redirect('onCourse:hod_dashboard')
    else:
        form = HODMessageForm()

    context = {
        'total_learners': total_learners,
        'average_performance': total_grasp_levels.get('avg_grasp_level', 0),
        'reports_submitted': reports_submitted,
        'subjects': subjects,
        'learner_progress': learner_progress,
        'underperforming_learners': underperforming_learners,
        'form': form,
    }
    return render(request, 'onCourse/hod_views.html', context)

def HOD_Correspondence(request):
    messages = HODMessage.objects.filter()
    context = {'messages': messages}
    return render(request, 'onCourse/HOD_Correspondence.html', context)

def district_dashboard(request):
    return render(request, 'onCourse/district_dashboard.html')

def district_views(request):
    # Get filter parameters
    school_id = request.GET.get('schoolFilter')
    subject_id = request.GET.get('subjectFilter')
    date_start = request.GET.get('dateStartFilter')
    date_end = request.GET.get('dateEndFilter')

    # Base queryset
    queryset = SchoolProgress.objects.all()

    # Apply filters
    if school_id:
        queryset = queryset.filter(school_id=school_id)
    if subject_id:
        queryset = queryset.filter(subject_id=subject_id)
    if date_start:
        start_date = parse_date(date_start)
        queryset = queryset.filter(date__gte=start_date)
    if date_end:
        end_date = parse_date(date_end)
        queryset = queryset.filter(date__lte=end_date)

    # Aggregated metrics
    total_schools = School.objects.count()
    average_district_performance = queryset.aggregate(Avg('performance_score'))['performance_score__avg'] or 0
    reports_submitted = queryset.count()

    # Data for table
    school_progress_list = queryset.select_related('school', 'subject', 'concept')

    # Data for charts (ensure 0 for schools with no data)
    school_performance = queryset.values('school__name').annotate(
        average_performance=Avg('performance_score')
    ).order_by('school__name')
    
    district_performance = queryset.values('date__week').annotate(
        average_performance=Avg('performance_score')
    ).order_by('date__week')

    # Prepare chart data
    school_labels = [sp['school__name'] for sp in school_performance]
    school_data = [sp['average_performance'] or 0 for sp in school_performance]  # Handle None cases

    district_labels = [f"Week {dp['date__week']}" for dp in district_performance]
    district_data = [dp['average_performance'] or 0 for dp in district_performance]  # Handle None cases

    context = {
        'schools': School.objects.all(),
        'subjects': Subject.objects.all(),
        'total_schools': total_schools,
        'average_district_performance': average_district_performance,
        'reports_submitted': reports_submitted,
        'school_progress_list': school_progress_list,
        'school_labels': school_labels,
        'school_data': school_data,
        'district_labels': district_labels,
        'district_data': district_data,
    }
    return render(request, 'onCourse/district_views.html', context)

def submit_answers(request):
    concept = get_object_or_404(Concept)
    # Retrieve the Learner object associated with the logged-in user
    learner = get_object_or_404(Learner)

    if request.method == 'POST':
        q1_answer = request.POST.get('question1')
        q2_answer = request.POST.get('question2')

        # Assuming each question has an associated correct answer
        q1_correct = concept.question1.correct_choice.id
        q2_correct = concept.question2.correct_choice.id

        correct_count = 0
        if q1_answer == str(q1_correct):
            correct_count += 1
        if q2_answer == str(q2_correct):
            correct_count += 1
        # Determine the grade based on correct answers
        if correct_count == 0:
            grade = 'low'
        elif correct_count == 1:
            grade = 'medium'
        else:
            grade = 'high'

        # Save the grade
        LearnerGrade.objects.create(
            learner=learner,
            concept=concept,
            grade=grade
        )
        return redirect('onCourse:learner_grades')  # Redirect to the learner's grades page after submission
    context = {'concept': concept}
    return render(request, 'onCourse/submit_answers.html', context)
    
def concept_detail(request, concept_id):
    concept = get_object_or_404(Concept, pk=concept_id)
    questions = Question.objects.filter(concept=concept)
    context = {'concept': concept, 'questions': questions}
    return render(request, 'onCourse/concept_detail.html', context)

def concept_list(request):
    concepts = Concept.objects.all()
    context = {'concepts': concepts}
    return render(request, 'onCourse/concept_list.html', context)

def learner_grade(request):
    learner = request.user.learner
    grades = LearnerGrade.objects.filter(learner=learner)

    context = {
        'grades': grades,
    }
    return render(request, 'onCourse/learner_grade.html', context)

# Initialize Africa's Talking
africastalking.initialize(username=settings.AFRICASTALKING_USERNAME, api_key=settings.AFRICASTALKING_API_KEY)
ussd = africastalking.USSD

@csrf_exempt
def ussd_callback(request):
    session_id = request.POST.get('sessionId')
    service_code = request.POST.get('serviceCode')
    phone_number = request.POST.get('phoneNumber')
    text = request.POST.get('text', '').strip()

    response = ""

    if text == "":
        response = "CON Welcome to the Progress Report Service\n"
        response += "1. Get Child's Progress Report\n"
    elif text == "1":
        # Retrieve child's progress report
        progress = LearnerProgress.objects.filter(parent__phone_number=phone_number).last()
        if progress:
            response = f"END Progress Report:\nSubject: {progress.subject.name}\nConcept: {progress.concept.name}\nGrasp Level: {progress.get_grasp_level_display()}"
        else:
            response = "END No progress report found for your child."

    return HttpResponse(response, content_type="text/plain")

@csrf_exempt
def whatsapp_callback(request):
    from_number = request.POST.get('From')
    body = request.POST.get('Body').strip().lower()

    response = MessagingResponse() 

    if body == "report":
        # Retrieve child's progress report
        progress = LearnerProgress.objects.filter(parent__phone_number=from_number.replace("whatsapp:", "")).last()
        if progress:
            message = f"Progress Report:\nSubject: {progress.subject.name}\nConcept: {progress.concept.name}\nGrasp Level: {progress.get_grasp_level_display()}"
        else:
            message = "No progress report found for your child."
        response.message(message)
    else:
        response.message("Send 'report' to get your child's progress report.")

    return HttpResponse(str(response), content_type="text/xml")

