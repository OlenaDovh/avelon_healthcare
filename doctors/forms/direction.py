from __future__ import annotations

from django import forms

from doctors.models import Direction


class DirectionForm(forms.ModelForm):
    class Meta:
        model = Direction
        fields = ("name", "description")
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
        }