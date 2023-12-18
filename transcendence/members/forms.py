from django import forms
from .models import Player

class RegistrationForm(forms.ModelForm):
	class Meta:
		model = Player
		fields = ['name', 'email', 'password']
	def clean(self):
		if password != passwordConfirmation:
			raise forms.ValidationError("Passwords ndo not match.")