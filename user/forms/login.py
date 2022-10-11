from django import forms


#Neste caso não iremos utilizar um formulário atrelado a um model, ou seja, um Model.Form
#nos iremos utilizar um Form.
class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Seu usuário'
        }),
        label='Usuário'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Sua senha'
        }),
        label='Senha'
    )
