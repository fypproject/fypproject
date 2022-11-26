from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from .models import myAdmin,User,Faculty




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
    first_name=forms.CharField(required=True)
    email=forms.EmailField(required=True)

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