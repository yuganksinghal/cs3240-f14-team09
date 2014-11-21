from django import forms

class BulletinForm(forms.Form):
    author = forms.CharField(label="Author", max_length=100)
    description = forms.CharField(label = "Description", max_length=200)
    pubdate = forms.DateField()
    files = forms.FileField(upload_to='/Bulletins/user/%Y/%m/%d')
