from django.forms import ModelForm, DateInput
from calender.models import Event
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User, Group

from .models import *


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин',
                               widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Your username'}))
    email = forms.EmailField(label='Email',
                             widget=forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Your email'}))
    password1 = forms.CharField(label='Пароль',
                                widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Password'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(
        attrs={'class': 'form-input', 'placeholder': 'Repeat password'}))

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'placeholder': 'Your username'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'placeholder': 'Your password'}))

class AddForm(ModelForm):
    class Meta:
        model = Projects
        fields = ('worker', )


class AddForm1(ModelForm):
    project_name = forms.ChoiceField(choices=list(map(lambda a: (a[0], a[0]), Project.objects.all().values_list('project_name'))))
    class Meta:
        model = Projects
        fields = ('project_name', 'worker',)

class EventForm(ModelForm):
    project_name = forms.ChoiceField(choices=list(map(lambda a: (a[0], a[0]), Project.objects.all().values_list('project_name'))))
    status = forms.ChoiceField(choices=[('To Do', 'To Do'),  ('In progress', 'In progress'), ('Review', 'Review'), ('Done', 'Done')])
    class Meta:
        model = Event
        # datetime-local is a HTML5 input type, format to make date time show on fields
        widgets = {
            'start_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'end_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        }
        fields = ('title', 'description', 'start_time', 'end_time', 'project_name', 'status')

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        # input_formats to parse HTML5 datetime-local input to datetime field
        self.fields['start_time'].input_formats = ('%Y-%m-%dT%H:%M',)
        self.fields['end_time'].input_formats = ('%Y-%m-%dT%H:%M',)

class EventForm_NE(ModelForm):
    status = forms.ChoiceField(choices=[('To Do', 'To Do'),  ('In progress', 'In progress'), ('Review', 'Review'), ('Done', 'Done')])
    class Meta:
        model = Event
        # datetime-local is a HTML5 input type, format to make date time show on fields
        widgets = {
            'start_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'end_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        }
        fields = ('title', 'description', 'start_time', 'end_time', 'status')

    def __init__(self, *args, **kwargs):
        super(EventForm_NE, self).__init__(*args, **kwargs)
        # input_formats to parse HTML5 datetime-local input to datetime field
        self.fields['start_time'].input_formats = ('%Y-%m-%dT%H:%M',)
        self.fields['end_time'].input_formats = ('%Y-%m-%dT%H:%M',)
