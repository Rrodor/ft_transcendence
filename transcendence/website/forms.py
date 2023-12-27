from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm

class UserForm(UserCreationForm):
	class Meta(UserCreationForm.Meta):
		model = User
		fields = UserCreationForm.Meta.fields + ('email',)

class ChangePasswordForm(PasswordChangeForm):
	old_password = forms.CharField(widget=forms.PasswordInput, label='Old Password', help_text='Enter your old password')
	new_password1 = forms.CharField(widget=forms.PasswordInput, label='New Password', help_text='Enter your new password')
	new_password2 = forms.CharField(widget=forms.PasswordInput, label='Confirm Password', help_text='Confirm your new password')