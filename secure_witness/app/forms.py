from django import forms 
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class BulletinForm(forms.Form):
    title = forms.CharField(
        label = "Title",
        max_length = 50,
        required = True
    )
    
    description = forms.CharField(
        label = "Description", 
        max_length=200,
        required = True
    )
    
    password = forms.CharField(
        widget=forms.PasswordInput(),
        required = False
    )

    anonymous = forms.BooleanField(
        required=False, 
        label='Anonymous' 
    )
    
