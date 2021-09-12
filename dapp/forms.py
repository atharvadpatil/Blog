from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class contactForm(forms.Form):
    full_name=forms.CharField()
    email=forms.EmailField()
    content=forms.CharField(widget=forms.Textarea)

    def clean_email(self, *args, **kwargs):
        Email = self.cleaned_data.get('email')
        print(Email)
        if Email.endswith(".edu"):
            raise forms.ValidationError("Don't use .edu emails")
        return Email




class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']
