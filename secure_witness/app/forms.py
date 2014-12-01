from django import forms 
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class BulletinForm(forms.Form):
    description = forms.CharField(label = "Description", max_length=200)
    pubdate = forms.DateField(required=False)
    path = forms.FileField (
        label='Select a file',
        help_text='max. 42 megabytes'
    )

class EditBulletinForm(forms.Form):
    description = forms.CharField(label = "Description", max_length=200)
    pubdate = forms.DateField(required=False)
    path = forms.FileField (
        required=False,
        label='Select a file',
        help_text='max. 42 megabytes'
    )
    password