from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from .models import myAdmin,User,Faculty,Student,Batch




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
    email=forms.EmailField(required=True,widget=forms.TextInput(attrs={'class': 'form-control inputelement','placeholder':'Enter Email','type':'email'}))

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
    email=forms.EmailField(required=True,widget=forms.TextInput(attrs={'class': 'form-control inputelement','placeholder':'Enter Email','type':'email'}))
    s_regno=forms.CharField(required=True,widget=forms.TextInput(attrs={'class': 'form-control inputelement','placeholder':'Enter Registeration Number'}))
    s_batchid=forms.ModelChoiceField(queryset=Batch.objects.all(),widget=forms.Select(attrs={'class': 'form-control','':'helloooooo'}))
    class Meta(UserCreationForm.Meta):
        model = User

    
    def __init__(self, *args, **kwargs):
        super(studentSignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control inputelement','placeholder':'Enter Username'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control inputelement','placeholder':'Enter Password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control inputelement','placeholder':'Confirm Password '})
        # self.fields['s_batchid']=forms.ModelChoiceField(queryset=Batch.objects.all())
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.first_name=self.cleaned_data.get('first_name')
        user.email=self.cleaned_data.get('email')
        user.is_student = True
        user.save()
        student = Student.objects.create(user=user)
        student.s_regno=self.cleaned_data.get('s_regno')
        student.s_batchid=self.cleaned_data.get('s_batchid')
        student.save()

        return student
    def clean_s_regno(self):
        s_regno = self.cleaned_data['s_regno']
        if Student.objects.filter( s_regno=s_regno).exists():
            raise forms.ValidationError("Registration Number already exists")
        return s_regno
    