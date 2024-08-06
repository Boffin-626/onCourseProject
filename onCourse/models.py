from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

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

class Learner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='learner')
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('Parent', on_delete=models.CASCADE)
    school = models.ForeignKey('School', on_delete=models.CASCADE)

class LearnerProgress(models.Model):
    learner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='progress')
    concepts_grasped = models.TextField()
    concepts_not_grasped = models.TextField()
    period_start = models.DateField()
    period_end = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'LearnerProgress'

class ProgressReport(models.Model):
    learner = models.ForeignKey(Learner, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    concept = models.CharField(max_length=100)
    grasped = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class Parent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='parent')
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()

class School(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher')
    name = models.CharField(max_length=100)
    school = models.ForeignKey(School, on_delete=models.CASCADE)

class ConceptGrasp(models.Model):
    learner = models.ForeignKey(Learner, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    concept = models.CharField(max_length=100)
    grasped = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class USSDRequest(models.Model):
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE)
    request_type = models.CharField(max_length=100)  # e.g. "progress report"
    created_at = models.DateTimeField(auto_now_add=True)

class WhatsAppRequest(models.Model):
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE)
    request_type = models.CharField(max_length=100)  # e.g. "progress report"
    created_at = models.DateTimeField(auto_now_add=True)