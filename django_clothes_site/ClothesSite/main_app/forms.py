from django import forms
from .models import Clothes_Item
from django.contrib.admin import widgets
from django.contrib.auth.models import User


class Login_Form(forms.Form):
    username = forms.CharField(label='User Name', max_length=64)
    password = forms.CharField(widget=forms.PasswordInput())


class Clothes_Form(forms.ModelForm):

    class Meta:
        model = Clothes_Item
        fields = ['name', 'description', 'size', 'price', 'clothing_type', 'image', 'gender']
        widgets = {'gender': forms.HiddenInput()}

    def __init__(self, *args, **kwargs):
        super(Clothes_Form, self).__init__(*args, **kwargs)

class Feedback_Form(forms.Form):
    contact_name = forms.CharField(max_length=64)
    contact_email = forms.EmailField(max_length=64)
    content = forms.CharField(required=True, widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super(Feedback_Form, self).__init__(*args, **kwargs)
        self.fields['contact_name'].label = "Your name:"
        self.fields['contact_email'].label = "Your email:"
        self.fields['content'].label = "What do you want to say?"


class Signup_Form(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
