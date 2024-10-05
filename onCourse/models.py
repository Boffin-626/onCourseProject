from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from datetime import date, timedelta

from django.contrib.auth.models import User

class User(AbstractUser):
    TYPE_LEARNER = 'learner'
    TYPE_TEACHER = 'teacher'
    TYPE_PARENT = 'parent'
    USER_TYPES = (
        (TYPE_LEARNER, 'Learner'),
        (TYPE_TEACHER, 'Teacher'),
        (TYPE_PARENT, 'Parent')
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default=TYPE_LEARNER)

    groups = models.ManyToManyField(Group, related_name='oncourse_user_groups', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='oncourse_user_permissions')

class District(models.Model):
    name = models.CharField(max_length=255)
    region = models.CharField(max_length=255)  # Optional: Define a region or area the district covers

    def __str__(self):
        return self.name

class School(models.Model):
    name = models.CharField(max_length=255)
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='schools')
    address = models.CharField(max_length=255)
    principal = models.CharField(max_length=255)
    contact_email = models.EmailField()

    def __str__(self):
        return self.name

class SchoolEvent(models.Model):
    title = models.CharField(max_length=200)  # Event title
    description = models.TextField(blank=True, null=True)  # Event description (optional)
    start_date = models.DateTimeField()  # Event start date and time
    end_date = models.DateTimeField()  # Event end date and time

    def __str__(self):
        return self.title
    
class Subject(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher')
    name = models.CharField(max_length=100)
    subjects = models.ManyToManyField(Subject, related_name='teachers')
    school = models.ForeignKey(School, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Concept(models.Model):
    name = models.CharField(max_length=255)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.subject.name})"
    
class Question(models.Model):
    concept = models.ForeignKey(Concept, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=255)

    def __str__(self):
        return self.question_text
    
class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.answer_text

class Parent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='parent')
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()

class Learner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='learner')
    name = models.CharField(max_length=100)
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE, related_name='learners')
    school = models.ForeignKey('School', on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, related_name='learners', on_delete=models.CASCADE)
    background_info = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name

class LearnerInfo(models.Model):
    learner_name = models.ForeignKey(Learner, on_delete=models.CASCADE, related_name='learner')
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=60, choices=[('male', 'Male'), ('female', 'Female'), ('non-binary', 'Non-binary')])
    grade = models.CharField(max_length=20)
    extra_tutorials = models.BooleanField(default=False)
    previous_school = models.CharField(max_length=255)
    address = models.TextField()
    contact_number = models.CharField(max_length=20)
    email = models.EmailField()
    
    class Meta:
        verbose_name_plural = 'Learner Information'

    def __str__(self):
        return self.learner_name

def default_end_date():
    return date.today() + timedelta(days=14)

class ConceptGrasp(models.Model):
    learner = models.ForeignKey(Learner, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    concept = models.ForeignKey(Concept, on_delete=models.CASCADE)
    grasped = models.BooleanField(default=False)
    grasp_level = models.Choices
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.learner.name} - {self.concept.name} ({'Grasped' if self.grasped else 'Not Grasped'})"

class LearnerProgress(models.Model):
    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'

    GRASP_LEVEL_CHOICES = [
        (LOW, 'Low'),
        (MEDIUM, 'Medium'),
        (HIGH, 'High'),
    ]

    learner = models.ForeignKey(Learner, on_delete=models.CASCADE, related_name='progress')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    concept = models.ForeignKey(Concept, on_delete=models.CASCADE)
    grasp_level = models.CharField(
        max_length=6,
        choices=GRASP_LEVEL_CHOICES,
        default=LOW,
    )
    score = models.IntegerField(default=0)
    period_start = models.DateField(default=date.today)
    period_end = models.DateField(default=default_end_date)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'LearnerProgress'

class LearnerPerformance(models.Model):
    learner = models.ForeignKey(Learner, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    score = models.FloatField()
    date = models.DateField()
    grade = models.CharField(max_length=20)

class PerformanceAnalytics(models.Model):
    learner = models.ForeignKey(Learner, on_delete=models.CASCADE)
    average_score = models.FloatField()
    predicted_score = models.FloatField()
    comparison_to_average = models.TextField()
    last_updated = models.DateTimeField(auto_now=True)

class TeacherComment(models.Model):
    progress_report = models.ForeignKey(LearnerProgress, on_delete=models.CASCADE, related_name='comments')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class DistrictOffice(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    district = models.OneToOneField(District, on_delete=models.CASCADE, related_name='office')
    head = models.CharField(max_length=255)  # Head of the district office
    contact_email = models.EmailField(default='example@example.com')
    contact_phone = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.district.name} Office"

class USSDRequest(models.Model):
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE)
    request_type = models.CharField(max_length=100)  # e.g. "progress report"
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default="pending")
    response_message = models.TextField(blank=True, null=True)

class WhatsAppRequest(models.Model):
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE)
    request_type = models.CharField(max_length=100)  # e.g. "progress report"
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default="pending")
    response_message = models.TextField(blank=True, null=True)

class HOD(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='hod')
    school = models.ForeignKey('School', on_delete=models.CASCADE, related_name='hods')

    def __str__(self):
        return f'{self.user.username} - {self.school.name}'

class LearnerGrade(models.Model):
    learner = models.ForeignKey(Learner, on_delete=models.CASCADE)
    concept = models.ForeignKey(Concept, on_delete=models.CASCADE)
    grade = models.CharField(max_length=10, choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')])

    def __str__(self):
        return f'{self.learner} - {self.concept} - {self.grade}'

class SchoolProgress(models.Model):
    GRASP_LEVEL_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    school = models.ForeignKey(School, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    concept = models.ForeignKey(Concept, on_delete=models.CASCADE)
    grasp_level = models.CharField(max_length=10, choices=GRASP_LEVEL_CHOICES)
    performance_score = models.FloatField()  # Store performance percentage or other metric
    school_comment = models.TextField(blank=True, null=True)
    date = models.DateField()

    def __str__(self):
        return f"{self.school.name} - {self.subject.name} - {self.concept.name}"

    class Meta:
        ordering = ['-date']
        verbose_name = 'School Progress'
        verbose_name_plural = 'School Progress'

class HODMessage(models.Model):
    hod = models.ForeignKey(User, on_delete=models.CASCADE, related_name='hod_messages')
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='teacher_messages')
    learner_progress = models.ForeignKey('LearnerProgress', on_delete=models.CASCADE)
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE)
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Message from {self.hod} to {self.teacher} about {self.learner_progress.learner.name}'

