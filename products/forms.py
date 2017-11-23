from django import forms

class postForm(forms.Form):
    productname  = forms.CharField(required = True, max_length = 100)
    description  = forms.CharField(required = True, max_length = 200)
    quantity = forms.IntegerField(required = True)
    pic = forms.FileField(required = True)
