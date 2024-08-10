# forms.py
from django import forms
from .models import LearnerProgress, ConceptGrasp, USSDRequest, WhatsAppRequest, TeacherComment

class LearnerProgressForm(forms.ModelForm):
    class Meta:
        model = LearnerProgress
        fields = ['concepts_grasped', 'concepts_not_grasped', 'period_start', 'period_end']

class ConceptGraspForm(forms.ModelForm):
    class Meta:
        model = ConceptGrasp
        fields = ['subject', 'concept', 'grasped']

class USSDRequestForm(forms.ModelForm):
    class Meta:
        model = USSDRequest
        fields = ['request_type']

class WhatsAppRequestForm(forms.ModelForm):
    class Meta:
        model = WhatsAppRequest
        fields = ['request_type']

class TeacherCommentForm(forms.ModelForm):
    class Meta:
        model = TeacherComment
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Add your comment here...'}),
        }
