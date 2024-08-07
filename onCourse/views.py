# learner_views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import LearnerProgressForm
from .models import LearnerProgress
from django.contrib.auth.models import User
from twilio.rest import Client

def index(request):
    return render(request, 'onCourse/index.html')

@login_required
def learner_progress(request):
    if request.method != 'POST':
        form = LearnerProgressForm()
    else:
        form = LearnerProgressForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('onCourse:learner_progress_success')
    context = {'form': form}
    return render(request, 'onCourse/learner_progress.html', context)

def learner_progress_success(request):
    return render(request, 'onCourse/learner_progress_success.html')

def learner_analytics(request):
    learners = User.objects.filter(user_type=User.learner)
    learner_progresses = LearnerProgress.objects.all()
    return render(request, 'onCourse/learner_analytics.html', {'learners': learners, 'learner_progresses': learner_progresses})

def comparative_analytics(request):
    learners = User.objects.filter(user_type=User.TYPE_LEARNER)
    learner_progresses = LearnerProgress.objects.all()
    return render(request, 'onCourse/comparative_analytics.html', {'learners': learners, 'learner_progresses': learner_progresses})

def all_learners_analytics(request):
    learners = User.objects.filter(user_type=User.username)
    learner_progresses = LearnerProgress.objects.all()
    return render(request, 'onCourse/all_learners_analytics.html', {'learners': learners, 'learner_progresses': learner_progresses})

def send_sms_report(learner_progress):
    account_sid = 'your_account_sid'
    auth_token = 'your_auth_token'
    client = Client(account_sid, auth_token)

    parent_phone_number = learner_progress.learner.parent.phone_number
    message = client.messages.create(
        body=f"Your child, {learner_progress.learner.username}, has made progress in the following concepts: {learner_progress.concepts_grasped}. They struggled with: {learner_progress.concepts_not_grasped}.",
        from_='your_twilio_phone_number',
        to=parent_phone_number
    )

def ussd_request(request):
    # USSD API integration goes here
    pass

def whatsapp_request(request):
    # WhatsApp API integration goes here
    pass