from django import forms
from django.contrib.auth.models import User
from .models import Employee


class EmployeeRegistrationForm(forms.ModelForm):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Employee
        fields = ['username', 'password']

    def save(self, commit=True):
        user = User.objects.create_user(
            self.cleaned_data['username'],
            password=self.cleaned_data['password']
        )
        employee = super(EmployeeRegistrationForm, self).save(commit=False)
        employee.user = user
        if commit:
            employee.save()
        return employee
