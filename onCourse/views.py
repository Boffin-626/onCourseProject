# views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Learner, LearnerProgress, USSDRequest, WhatsAppRequest, Parent, School, Teacher, TeacherComment, HOD
from .forms import LearnerProgressForm, USSDRequestForm, WhatsAppRequestForm, TeacherCommentForm

from django.db.models import Sum, Count, Q, Avg
from django.shortcuts import render
from datetime import datetime

import csv
from django.http import HttpResponse

def index(request):
    return render(request, 'onCourse/index.html')

def learner_progress(request):
    learner = get_object_or_404(Learner)
    if request.method == 'POST':
        form = LearnerProgressForm(request.POST)
        if form.is_valid():
            progress = form.save(commit=False)
            progress.learner = learner
            progress.save()
            return redirect('onCourse:report_update')
    else:
        form = LearnerProgressForm()
    context = {'learner': learner, 'form': form}
    return render(request, 'onCourse/learner_progress.html', context)

def report_update(request):
    return render(request, 'onCourse/report_update.html')

def teacher_dashboard(request):
    # Example: Display all learners and their progress reports
    learners = Learner.objects.all()
    context = {
        'learners': learners
    }
    return render(request, 'onCourse/teacher_dashboard.html', context)

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
    parent = get_object_or_404(Parent)
    context = {'parent': parent}
    return render(request, 'onCourse/parent_dashboard.html', context)

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
    # Ensure request.user is used to get the HOD instance
    hod = get_object_or_404(HOD)
    school = hod.school
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    subject = request.GET.get('subject')

    # Initialize filters
    filters = Q(learner__school=school)

    # Apply date filters if provided
    if start_date and end_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        filters &= Q(created_at__range=[start_date, end_date])

    # Apply subject filters if provided
    if subject:
        filters &= Q(concept__subject=subject)

    # Query learner progress with the applied filters
    learner_progress = LearnerProgress.objects.filter(filters)
    teacher_comments = TeacherComment.objects.filter(progress_report__in=learner_progress)

    # Additional Analytics Logic
    total_learners = Learner.objects.filter(school=school).count()
    avg_grasped = learner_progress.aggregate(Avg('concepts_grasped'))
    avg_not_grasped = learner_progress.aggregate(Avg('concepts_not_grasped'))

    total_concepts_grasped = learner_progress.aggregate(total_grasped=Sum('concepts_grasped'))
    total_concepts_not_grasped = learner_progress.aggregate(total_not_grasped=Sum('concepts_not_grasped'))
    total_concepts = (total_concepts_grasped['total_grasped'] or 0) + (total_concepts_not_grasped['total_not_grasped'] or 0)

    grasped_percentage = (total_concepts_grasped['total_grasped'] / total_concepts) * 100 if total_concepts else 0
    not_grasped_percentage = (total_concepts_not_grasped['total_not_grasped'] / total_concepts) * 100 if total_concepts else 0

    comments_per_learner = teacher_comments.values('progress_report__learner').annotate(total_comments=Count('id'))

    # Prepare subject options for filtering
    subjects = learner_progress.values_list('subject', flat=True).distinct()

    # Prepare context for the template
    context = {
        'school': school,
        'learner_progress': learner_progress,
        'teacher_comments': teacher_comments,
        'avg_grasped': avg_grasped['concepts_grasped__avg'],
        'avg_not_grasped': avg_not_grasped['concepts_not_grasped__avg'],
        'grasped_percentage': grasped_percentage,
        'not_grasped_percentage': not_grasped_percentage,
        'comments_per_learner': comments_per_learner,
        'subjects': subjects,
    }
    return render(request, 'onCourse/hod_dashboard.html', context)

def export_to_csv(request):
    # Create a response object that can be used to write CSV data
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="learner_progress.csv"'

    # Create a CSV writer object
    writer = csv.writer(response)

    # Write the header row
    writer.writerow(['Learner', 'Concepts Grasped', 'Concepts Not Grasped', 'Date'])

    # Query the database for learner progress data
    learner_progress = LearnerProgress.objects.all()

    # Write data rows
    for progress in learner_progress:
        writer.writerow([progress.learner.user.username, progress.concepts_grasped, progress.concepts_not_grasped, progress.created_at])

    return response


