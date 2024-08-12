from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from datetime import date, timedelta

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
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} ({self.subject.name})"

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
    period_start = models.DateField(default=date.today)
    period_end = models.DateField(default=default_end_date)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'LearnerProgress'
    
    def __str__(self):
        return self.grasp_level

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

from django.db import models

