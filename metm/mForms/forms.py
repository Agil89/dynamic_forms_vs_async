from django import forms
from mForms.models import Values




class AllForms(forms.ModelForm):
    class Meta:
        model = Values
        fields = ('form_fields', 'value',)