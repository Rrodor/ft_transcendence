from django import forms
from .models import User
from django.utils.safestring import mark_safe
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm

class UserForm(UserCreationForm):
	avatar = forms.ImageField(label='Avatar', required=False, help_text=mark_safe('<br>Upload your avatar here'))
	class Meta(UserCreationForm.Meta):
		model = User
		fields = UserCreationForm.Meta.fields + ('email', 'avatar')

class ChangePasswordForm(PasswordChangeForm):
	old_password = forms.CharField(widget=forms.PasswordInput, label='Old Password', help_text='Enter your old password')
	new_password1 = forms.CharField(widget=forms.PasswordInput, label='New Password', help_text='Enter your new password')
	new_password2 = forms.CharField(widget=forms.PasswordInput, label='Confirm Password', help_text='Confirm your new password')

class ChangeAvatarForm(forms.ModelForm):
	avatar = forms.ImageField(label='Avatar', required=True, help_text=mark_safe('<br>Upload your avatar here'), widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))
	class Meta:
		model = User
		fields = ['avatar']