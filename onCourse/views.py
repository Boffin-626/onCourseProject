# views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Learner, LearnerProgress, USSDRequest, WhatsAppRequest, Parent, School, Teacher, TeacherComment, HOD, Concept, Subject, Concept, District, DistrictOffice
from .forms import LearnerProgressForm, ConceptGraspForm, USSDRequestForm, WhatsAppRequestForm, TeacherCommentForm

from django.db.models import Sum, Count, Q, Avg
from django.shortcuts import render
from datetime import datetime

from django.http import HttpResponse


def index(request):
    return render(request, 'onCourse/index.html')

def learner_progress_form(request, learner_id):
    # Retrieve a single learner object or raise a 404 error if not found
    learner = get_object_or_404(Learner, id=learner_id)

    if request.method == 'POST':
        form = LearnerProgressForm(request.POST)
        if form.is_valid():
            progress = form.save(commit=False)
            progress.learner = learner
            progress.save()
            # Redirect to a detail view or another page, passing the learner_id
            return redirect('onCourse:learner_progress_detail', learner_id=learner_id)
    else:
        # Initialize the form with the learner instance
        form = LearnerProgressForm()

    context = {
        'form': form, 
        'learner': learner
    }
    return render(request, 'onCourse/learner_progress_form.html', context)

def learner_progress_detail(request, learner_id):
    learner = get_object_or_404(Learner, id=learner_id)
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


from django.shortcuts import render, get_object_or_404
from .models import Teacher, LearnerProgress

def teacher_dashboard(request):
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

    # Get filter parameters
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    subject_id = request.GET.get('subject')

    # Initialize filters
    filters = Q(learner__school=school)

    # Apply date filters if provided
    if start_date and end_date:
        filters &= Q(created_at__range=[start_date, end_date])

    # Apply subject filter if provided
    if subject_id:
        filters &= Q(subject_id=subject_id)

    # Filter LearnerProgress records based on filters
    learner_progress = LearnerProgress.objects.filter(filters)

    # Calculate grasp level distribution
    grasp_level_distribution = learner_progress.values('grasp_level').annotate(count=Count('grasp_level'))

    # Aggregate grasp levels by subject
    subject_grasp_levels = learner_progress.values('subject__name', 'grasp_level').annotate(count=Count('grasp_level'))

    # Prepare subject options for filtering
    subjects = Subject.objects.filter()

    # Prepare context for the template
    context = {
        'school': school,
        'learner_progress': learner_progress,
        'grasp_level_distribution': grasp_level_distribution,
        'subject_grasp_levels': subject_grasp_levels,
        'subjects': subjects,
    }
    return render(request, 'onCourse/hod_dashboard.html', context)

def district_dashboard(request):
    district_office = get_object_or_404(DistrictOffice)
    schools = School.objects.filter(district=district_office.district)

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    subject = request.GET.get('subject')

    # Initialize filters
    filters = Q(learner__school__in=schools)

    # Apply date filters if provided
    if start_date and end_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        filters &= Q(created_at__range=[start_date, end_date])

    # Apply subject filters if provided
    if subject:
        filters &= Q(subject__name=subject)

    # Query learner progress with the applied filters
    learner_progress = LearnerProgress.objects.filter(filters)

    # Aggregated data analytics for the district
    total_learners = learner_progress.values('learner').distinct().count()
    avg_grasp_level = learner_progress.aggregate(avg_grasp=Avg('grasp_level'))
    learners_by_grasp_level = learner_progress.values('grasp_level').annotate(count=Count('id'))

    # Retrieve subjects taught in the district
    subjects = Subject.objects.filter(
        id__in=learner_progress.values_list('subject_id', flat=True)
    ).distinct()

    context = {
        'schools': schools,
        'total_learners': total_learners,
        'avg_grasp_level': avg_grasp_level['avg_grasp'],
        'learners_by_grasp_level': learners_by_grasp_level,
        'subjects': subjects,
    }
    return render(request, 'onCourse/district_dashboard.html', context)


