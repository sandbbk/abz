from django import forms
from .models import Employee


class EmpForm(forms.ModelForm):

    class Meta:
        model = Employee
        fields = ('full_name', 'emp_position', 'chief', 'date_of_recruit', 'salary', 'photo')
