# forms.py
from django import forms
from .models import *

class LearnerInfoForm(forms.ModelForm):
    class Meta:
        model = LearnerInfo
        fields = ['learner_name', 'date_of_birth', 'gender', 'grade', 'extra_tutorials', 'previous_school', 'address', 'contact_number', 'email']

class LearnerProgressForm(forms.ModelForm):
    class Meta:
        model = LearnerProgress
        fields = ['concept', 'grasp_level']
        widgets = {
            'grasp_level': forms.RadioSelect(choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')]),
        }

    def __init__(self, *args, **kwargs):
        super(LearnerProgressForm, self).__init__(*args, **kwargs)
        self.fields['concept'].queryset = Concept.objects.none()

        if 'subject' in self.data:
            try:
                subject_id = int(self.data.get('subject'))
                self.fields['concept'].queryset = Concept.objects.filter(subject_id=subject_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty concept queryset
        elif self.instance.pk:
            self.fields['concept'].queryset = self.instance.subject.concept_set.order_by('name')

class SchoolReportUploadForm(forms.Form):
    report_image = forms.ImageField()
    
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

class HODMessageForm(forms.ModelForm):
    class Meta:
        model = HODMessage
        fields = ['teacher', 'subject', 'message']
        widgets = {
            'teacher': forms.Select(attrs={'class': 'form-control'}),
            'subject': forms.Select(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }
