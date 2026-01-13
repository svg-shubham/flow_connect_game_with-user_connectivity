from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class ProfessionalSignupForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='Aapka asli naam')
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=254, required=True, help_text='Zaruri hai password reset ke liye')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email')