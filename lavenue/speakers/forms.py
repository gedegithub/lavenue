from django import forms
from motions.models import Motion
from django.forms import ModelForm

from .models import Intervention
from django.contrib.admin.widgets import AdminTimeWidget

class InterventionForm(ModelForm):
    class Meta:
        model = Intervention
        fields = '__all__'


class MotionForm(ModelForm):
    class Meta:
        model = Motion
        fields = '__all__'


