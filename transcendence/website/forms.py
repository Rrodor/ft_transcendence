from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm

class UserForm(UserCreationForm):
	class Meta(UserCreationForm.Meta):
		model = User
		fields = UserCreationForm.Meta.fields + ('email',)