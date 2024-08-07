from django import forms
from .models import LearnerProgress

class LearnerProgressForm(forms.ModelForm):
    class Meta:
        model = LearnerProgress
        fields = ('concepts_grasped', 'concepts_not_grasped', 'period_start', 'period_end')