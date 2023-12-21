from django import forms
from django.contrib.auth.models import User

class RegistrationForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'password']
	def clean(self):
		if password != passwordConfirmation:
			raise forms.ValidationError("Passwords ndo not match.")
