from django import forms
from django.core.exceptions import ValidationError
from utils.django_form import email_validate, strong_password


class ChangePasswordForm(forms.Form):
    
    first_name = forms.CharField(
        error_messages={'required': 'Escreva seu nome'},
        label='Edite seu nome',
        min_length=3, max_length=20,
    )
    last_name = forms.CharField(
        error_messages={'required': 'Escreva seu sobrenome'},
        label='Edite seu sobrenome',
        min_length=2, max_length=100, 
    )

    password = forms.CharField(
        widget=forms.PasswordInput(),
        label='Senha nova',
        help_text = ('A senha deve ter pelo menos uma letra, um número e ter no mínimo 8 caracteres.'),
        validators = [strong_password]
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(),
        label='Confirme a nova senha'
    )

    def clean(self):
        
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password != password2:
            password_confirmation_error = ValidationError(
                'As senhas estão diferentes, por favor digite-as novamente',
                code='invalid'
            )
            raise ValidationError({
                'password': password_confirmation_error,
                'password2': password_confirmation_error
            })

        return cleaned_data
