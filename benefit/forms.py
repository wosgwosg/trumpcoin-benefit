from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile, BankDetails, Application

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        if commit:
            user.save()
        return user

class UserProfileForm(forms.ModelForm):
    dob = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Date of Birth'
    )
    
    class Meta:
        model = UserProfile
        fields = ('phone', 'address', 'dob', 'country', 'ssn_or_id')
        labels = {
            'ssn_or_id': 'Social Security Number or ID',
        }

class BankDetailsForm(forms.ModelForm):
    class Meta:
        model = BankDetails
        fields = ('bank_name', 'account_number', 'routing_number', 'amount_to_apply')
        widgets = {
            'account_number': forms.TextInput(attrs={'placeholder': 'Enter your account number'}),
            'routing_number': forms.TextInput(attrs={'placeholder': 'Enter your routing number'}),
        }

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    subject = forms.CharField(max_length=200, required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)
