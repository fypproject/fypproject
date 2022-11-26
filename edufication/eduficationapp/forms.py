from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from .models import myAdmin,User,Faculty,Student




class myAdminSignUpForm(UserCreationForm):
    first_name=forms.CharField(required=True)
    email=forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.first_name=self.cleaned_data.get('first_name')
        user.email=self.cleaned_data.get('email')
        user.is_myadmin = True
        user.save()
        myadmin = myAdmin.objects.create(user=user)
        myadmin.save()

        return myadmin



class facultySignUpForm(UserCreationForm):
    first_name=forms.CharField(required=True,widget=forms.TextInput(attrs={'class': 'form-control inputelement','placeholder':'Enter Name'}))
    email=forms.EmailField(required=True,widget=forms.TextInput(attrs={'class': 'form-control inputelement','placeholder':'Enter Email'}))

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.first_name=self.cleaned_data.get('first_name')
        user.email=self.cleaned_data.get('email')
        user.is_faculty = True
        user.save()
        faculty = Faculty.objects.create(user=user)
        faculty.save()

        return faculty
    def __init__(self, *args, **kwargs):
        super(facultySignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control inputelement','placeholder':'Enter Username'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control inputelement','placeholder':'Enter Password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control inputelement','placeholder':'Confirm Password '})

class studentSignUpForm(UserCreationForm):
    first_name=forms.CharField(required=True,widget=forms.TextInput(attrs={'class': 'form-control inputelement','placeholder':'Enter Name'}))
    email=forms.EmailField(required=True,widget=forms.TextInput(attrs={'class': 'form-control inputelement','placeholder':'Enter Email'}))
    s_regno=forms.CharField(required=True,widget=forms.TextInput(attrs={'class': 'form-control inputelement','placeholder':'Enter Registeration Number'}))
    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.first_name=self.cleaned_data.get('first_name')
        user.email=self.cleaned_data.get('email')
        user.is_student = True
        user.save()
        student = Student.objects.create(user=user)
        student.s_regno=self.cleaned_data.get('s_regno')
        student.save()

        return student
    def __init__(self, *args, **kwargs):
        super(studentSignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control inputelement','placeholder':'Enter Username'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control inputelement','placeholder':'Enter Password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control inputelement','placeholder':'Confirm Password '})