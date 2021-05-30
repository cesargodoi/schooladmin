from django import forms
from schooladmin.common import HIDDEN_AUTH_FIELDS

from .models import Seeker, Lecture, Listener, Historic


class SeekerForm(forms.ModelForm):
    class Meta:
        model = Seeker
        fields = "__all__"
        widgets = {
            "observations": forms.Textarea(attrs={"rows": 2}),
            "birth": forms.widgets.DateInput(
                format="%Y-%m-%d", attrs={"type": "date"}
            ),
        }
        widgets.update(HIDDEN_AUTH_FIELDS)


class LectureForm(forms.ModelForm):
    class Meta:
        model = Lecture
        fields = "__all__"
        exclude = ["listeners"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 2}),
            "date": forms.widgets.DateInput(
                format="%Y-%m-%d", attrs={"type": "date"}
            ),
        }
        widgets.update(HIDDEN_AUTH_FIELDS)


class ListenerForm(forms.ModelForm):
    class Meta:
        model = Listener
        fields = ["ranking", "observations"]
        widgets = {
            "ranking": forms.widgets.NumberInput(attrs={"min": 0, "max": 2}),
        }


class HistoricForm(forms.ModelForm):
    class Meta:
        model = Historic
        exclude = ["listeners"]
        widgets = {
            "descriptions": forms.Textarea(attrs={"rows": 2}),
            "date": forms.widgets.DateInput(
                format="%Y-%m-%d", attrs={"type": "date"}
            ),
            "seeker": forms.HiddenInput(),
        }
        widgets.update(HIDDEN_AUTH_FIELDS)
