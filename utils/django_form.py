import re

from django.core.exceptions import ValidationError


def strong_password(password):
    regex = re.compile(r'^(?=.*[a-z])(?=.*[0-9]).{8,}$')

    if not regex.match(password):
        raise ValidationError(
            ('A senha deve ter pelo menos uma letra, um número e ter no mínimo 8 caracteres.'),
            code = 'invalid'
            
        )

def email_validate(email):
    regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
    
    if not regex.match(email):
        raise ValidationError(
            code='invalid'
        )
