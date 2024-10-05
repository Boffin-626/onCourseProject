from django.contrib import admin
from .models import *

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'user_type', 'is_staff', 'is_active']
    search_fields = ['username', 'email', 'user_type']
    list_filter = ['user_type', 'is_staff', 'is_active']

@admin.register(Learner)
class LearnerAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'parent', 'school']
    search_fields = ['name', 'user__username', 'parent__name', 'school__name']
    list_filter = ['school']

admin.site.register(LearnerProgress)
admin.site.register(SchoolProgress)

  

@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'phone_number', 'email']
    search_fields = ['name', 'user__username', 'phone_number', 'email']

@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ['name', 'address']
    search_fields = ['name', 'address']

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'school']
    search_fields = ['name', 'user__username', 'school__name']
    list_filter = ['school']

@admin.register(TeacherComment)
class TeacherCommentAdmin(admin.ModelAdmin):
    list_display = ['progress_report', 'teacher', 'comment', 'created_at']
    search_fields = ['progress_report__learner__name', 'teacher__name', 'comment']
    list_filter = ['created_at']

@admin.register(ConceptGrasp)
class ConceptGraspAdmin(admin.ModelAdmin):
    list_display = ['learner', 'subject', 'concept', 'grasped', 'created_at']
    search_fields = ['learner__name', 'subject', 'concept']
    list_filter = ['subject', 'grasped', 'created_at']

@admin.register(USSDRequest)
class USSDRequestAdmin(admin.ModelAdmin):
    list_display = ['parent', 'request_type', 'created_at', 'status']
    search_fields = ['parent__name', 'request_type']
    list_filter = ['status', 'created_at']

@admin.register(WhatsAppRequest)
class WhatsAppRequestAdmin(admin.ModelAdmin):
    list_display = ['parent', 'request_type', 'created_at', 'status']
    search_fields = ['parent__name', 'request_type']
    list_filter = ['status', 'created_at']

@admin.register(HOD)
class HODAdmin(admin.ModelAdmin):
    list_display = ['user', 'school']
    search_fields = ['user__username', 'school__name']
    list_filter = ['school']
    
admin.site.register(LearnerInfo)
admin.site.register(Subject)
admin.site.register(Concept)
admin.site.register(District)
admin.site.register(DistrictOffice)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(LearnerGrade)
admin.site.register(HODMessage)
admin.site.register(SchoolEvent)
admin.site.register(LearnerPerformance)
admin.site.register(PerformanceAnalytics)
