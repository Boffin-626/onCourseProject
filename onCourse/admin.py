from django.contrib import admin
from .models import User, Learner, LearnerProgress, Parent, School, Teacher, ConceptGrasp, USSDRequest, WhatsAppRequest, TeacherComment, HOD

# Register the User model with custom display settings
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'user_type', 'is_staff')
    list_filter = ('user_type', 'is_staff')
    search_fields = ('username', 'email')
    ordering = ('username',)

# Register the Learner model
@admin.register(Learner)
class LearnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'school', 'parent')
    list_filter = ('school',)
    search_fields = ('name', 'user__username', 'school__name')

# Register the LearnerProgress model
@admin.register(LearnerProgress)
class LearnerProgressAdmin(admin.ModelAdmin):
    list_display = ('learner', 'period_start', 'period_end', 'created_at')
    list_filter = ('period_start', 'period_end', 'learner__school')
    search_fields = ('learner__name', 'concepts_grasped', 'concepts_not_grasped')

@admin.register(TeacherComment)
class TeacherCommentAdmin(admin.ModelAdmin):
    list_display = ('progress_report', 'teacher', 'created_at')
    search_fields = ('progress_report__learner__name', 'teacher__username')
    list_filter = ('created_at',)

# Register the Parent model
@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'phone_number', 'email')
    search_fields = ('name', 'user__username', 'phone_number', 'email')

# Register the School model
@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ('name', 'address')
    search_fields = ('name', 'address')

# Register the Teacher model
@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'school')
    list_filter = ('school',)
    search_fields = ('name', 'user__username', 'school__name')

# Register the ConceptGrasp model
@admin.register(ConceptGrasp)
class ConceptGraspAdmin(admin.ModelAdmin):
    list_display = ('learner', 'subject', 'concept', 'grasped', 'created_at')
    list_filter = ('subject', 'grasped')
    search_fields = ('learner__name', 'subject', 'concept')

# Register the USSDRequest model
@admin.register(USSDRequest)
class USSDRequestAdmin(admin.ModelAdmin):
    list_display = ('parent', 'request_type', 'created_at')
    search_fields = ('parent__name', 'request_type')

# Register the WhatsAppRequest model
@admin.register(WhatsAppRequest)
class WhatsAppRequestAdmin(admin.ModelAdmin):
    list_display = ('parent', 'request_type', 'created_at')
    search_fields = ('parent__name', 'request_type')

@admin.register(HOD)
class HODAdmin(admin.ModelAdmin):
    list_display = ('user', 'school')