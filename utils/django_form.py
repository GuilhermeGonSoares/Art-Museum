import re

from django.core.exceptions import ValidationError


def strong_password(password):
    regex = re.compile(r'^(?=.*[a-z])(?=.*[0-9]).{8,}$')

    if not regex.match(password):
        raise ValidationError(
            ('A senha deve ter pelo menos uma letra, um número e ter no mínimo 8 caracteres.'),
            code = 'invalid'
            
        )
