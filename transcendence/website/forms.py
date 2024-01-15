from django import forms
from .models import User
from django.utils.safestring import mark_safe
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.forms.widgets import ClearableFileInput

class UserForm(UserCreationForm):
    avatar = forms.ImageField(label='Avatar', required=False, help_text=mark_safe('<br>Upload your avatar here'))
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email', 'avatar')

from django import forms
from django.contrib.auth.forms import PasswordChangeForm

class ChangePasswordFormEn(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(ChangePasswordFormEn, self).__init__(*args, **kwargs)

        self.fields['old_password'].label = 'Old password'
        self.fields['old_password'].help_text = 'Enter your old password'

        self.fields['new_password1'].label = 'New password'
        self.fields['new_password1'].help_text = 'Enter your new password'

        self.fields['new_password2'].label = 'Confirmation'
        self.fields['new_password2'].help_text = 'Confirm your password'

class ChangePasswordFormFr(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(ChangePasswordFormFr, self).__init__(*args, **kwargs)

        self.fields['old_password'].label = 'Ancien mot de passe'
        self.fields['old_password'].help_text = 'Entrer votre ancien mot de passe'

        self.fields['new_password1'].label = 'Nouveau mot de passe'
        self.fields['new_password1'].help_text = 'Entrer votre nouveau mot de passe'

        self.fields['new_password2'].label = 'Confirmation'
        self.fields['new_password2'].help_text = 'Confirmez votre mot de passe'

class ChangePasswordFormSp(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(ChangePasswordFormSp, self).__init__(*args, **kwargs)

        self.fields['old_password'].label = 'Antigua contraseña'
        self.fields['old_password'].help_text = 'Ingrese su antigua contraseña'

        self.fields['new_password1'].label = 'Nueva contraseña'
        self.fields['new_password1'].help_text = 'Ingrese su nueva contraseña'

        self.fields['new_password2'].label = 'Confirmación'
        self.fields['new_password2'].help_text = 'Confirme su contraseña'

class CustomClearableFileInputEn(ClearableFileInput):
    template_name = 'custom_clearable_file_inputEn.html'

class CustomClearableFileInputFr(ClearableFileInput):
    template_name = 'custom_clearable_file_inputFr.html'

class CustomClearableFileInputSp(ClearableFileInput):
    template_name = 'custom_clearable_file_inputSp.html'

class ChangeAvatarFormEn(forms.ModelForm):
    avatar = forms.ImageField(label='Your Avatar', required=True, widget=CustomClearableFileInputEn(attrs={'class': 'form-control'}), )
    class Meta:
        model = User
        fields = ['avatar']

class ChangeAvatarFormFr(forms.ModelForm):
    avatar = forms.ImageField(label='Your Avatar', required=True, widget=CustomClearableFileInputFr())
    class Meta:
        model = User
        fields = ['avatar']

class ChangeAvatarFormSp(forms.ModelForm):
    avatar = forms.ImageField(label='Your Avatar', required=True, widget=CustomClearableFileInputSp())
    class Meta:
        model = User
        fields = ['avatar']