from __future__ import annotations
from django import forms
from .models import Analysis

class AnalysisForm(forms.ModelForm):
    """Описує клас `AnalysisForm`."""

    class Meta:
        """Описує клас `Meta`."""
        model = Analysis
        fields = ('name', 'what_to_check', 'disease', 'for_whom', 'biomaterial', 'duration_days', 'price', 'is_active')
        widgets = {'name': forms.TextInput(attrs={'class': 'form-control'}), 'what_to_check': forms.TextInput(attrs={'class': 'form-control'}), 'disease': forms.TextInput(attrs={'class': 'form-control'}), 'for_whom': forms.TextInput(attrs={'class': 'form-control'}), 'biomaterial': forms.TextInput(attrs={'class': 'form-control'}), 'duration_days': forms.NumberInput(attrs={'class': 'form-control'}), 'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}), 'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'})}
