from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from utils.django_form import strong_password


class RegisterForm(forms.ModelForm):
    username = forms.CharField(
        label='Usuário',
        help_text=( 
            'Usuário pode ter letras, números e um desses caracteres @.+-_'
            'O tamanho deve ser entre 4 e 20 caracteres'
            
        ),
        error_messages={
            'required': 'Este campo não pode ser vazio',
            'min_length': 'Usuário deve ter no mínimo 4 caracteres',
            'max_length': 'Usuário pode ter no máximo 20 caracteres',
        },
        min_length=4, max_length=20,
        widget= forms.TextInput(
            attrs={
                'placeholder': 'Seu usuário'
            }
        )
    )
    first_name = forms.CharField(
        error_messages={'required': 'Escreva seu nome'},
        label='Nome',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Ex.: Rafael'
            }
        )
    )
    last_name = forms.CharField(
        error_messages={'required': 'Escreva seu sobrenome'},
        label='Sobrenome',
        widget = forms.TextInput(
            attrs={
                'placeholder': 'Ex.: Lima'
            }
        )
    )
    password = forms.CharField(
        widget = forms.PasswordInput(),
        error_messages = {
            'required': 'A senha não pode ser vazia.'
        },
        help_text = ('A senha deve ter pelo menos uma letra, um número e ter no mínimo 8 caracteres.'),
        label = 'Senha',
        validators = [strong_password]
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(),
        label='Confirmar senha',
        error_messages={
            'required': 'Por favor, repita sua senha'
        }
    )

    email = forms.EmailField(
        error_messages = {'required': 'E-mail não pode ser vazio'},
        label = 'E-mail',
        help_text = 'E-mail precisa ser válido.',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Ex.: email@email.com'
            }
        )
    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
        ]

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password != password2:
            password_confirmation_error = ValidationError(
                'As senhas estão diferentes, por favor digite-as novamente'
            )
            raise ValidationError({
                'password': password_confirmation_error,
                'password2': password_confirmation_error
            })
    