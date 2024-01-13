from django import forms
from .models import User
from django.utils.safestring import mark_safe
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm

class UserForm(UserCreationForm):
    avatar = forms.ImageField(label='Avatar', required=False, help_text=mark_safe('<br>Upload your avatar here'))
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email', 'avatar')

from django import forms
from django.contrib.auth.forms import PasswordChangeForm

class ChangePasswordForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

        if user and user.language == 'fr':
            self.fields['old_password'].label = 'Ancien mot de passe'
            self.fields['old_password'].help_text = 'Entrer votre ancien mot de passe'

            self.fields['new_password1'].label = 'Nouveau mot de passe'
            self.fields['new_password1'].help_text = 'Entrer votre nouveau mot de passe'

            self.fields['new_password2'].label = 'Confirmation'
            self.fields['new_password2'].help_text = 'Confirmez votre mot de passe'
        elif user and user.language == 'sp':
            self.fields['old_password'].label = 'Antigua contraseña'
            self.fields['old_password'].help_text = 'Ingrese su antigua contraseña'

            self.fields['new_password1'].label = 'Nueva contraseña'
            self.fields['new_password1'].help_text = 'Ingrese su nueva contraseña'

            self.fields['new_password2'].label = 'Confirmación'
            self.fields['new_password2'].help_text = 'Confirme su contraseña'


class ChangeAvatarForm(forms.ModelForm):
    avatar = forms.ImageField(label='Avatar', required=True, help_text=mark_safe('<br>Upload your avatar here'), widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))
    class Meta:
        model = User
        fields = ['avatar']