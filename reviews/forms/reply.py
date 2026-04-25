from __future__ import annotations
from django import forms
from reviews.models import Review

class ReviewReplyForm(forms.ModelForm):
    """Описує клас `ReviewReplyForm`."""

    class Meta:
        """Описує клас `Meta`."""
        model = Review
        fields = ('clinic_reply',)
        widgets = {'clinic_reply': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Введіть відповідь на відгук'})}
        labels = {'clinic_reply': 'Відповідь клініки'}
