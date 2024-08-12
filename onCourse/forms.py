# forms.py
from django import forms
from .models import LearnerProgress, ConceptGrasp, USSDRequest, WhatsAppRequest, TeacherComment, Subject, Concept

class LearnerProgressForm(forms.ModelForm):
    class Meta:
        model = LearnerProgress
        fields = ['learner', 'subject', 'concept', 'grasp_level', 'period_start', 'period_end']
        widgets = {
            'period_start': forms.DateInput(attrs={'type': 'date'}),
            'period_end': forms.DateInput(attrs={'type': 'date'}),
        }

class ConceptGraspForm(forms.ModelForm):
    subject = forms.ModelChoiceField(queryset=Subject.objects.all(), required=True)
    concept = forms.ModelChoiceField(queryset=Concept.objects.none(), required=True)
    
    class Meta:
        model = ConceptGrasp
        fields = ['subject', 'concept', 'grasped']

    def __init__(self, *args, **kwargs):
        subject_id = kwargs.pop('subject_id', None)
        super(ConceptGraspForm, self).__init__(*args, **kwargs)
        if subject_id:
            self.fields['concept'].queryset = Concept.objects.filter(subject_id=subject_id)
        else:
            self.fields['concept'].queryset = Concept.objects.none()

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
