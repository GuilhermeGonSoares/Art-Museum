import re

from django.core.exceptions import ValidationError
from django.db.models import Q
from genericpath import exists
from museum.models import *


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

def date_validade(date):
    regex = re.compile(r'^(((([1-9]|[0-2][0-9]|(3)[0-1])(\/))?(([1-9]|(0)[0-9])|((1)[0-2]))(\/))?\d{4})|M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})$')

    if not regex.match(date):
        raise ValidationError(
            ('Formato de data não aceito, Por favor insira um formato válido.'),
            code='invalid'
        )
    if regex.match(date):
        if len(regex.match(date).group()) != len(date):
            raise ValidationError(
            ('Formato de data não aceito, Por favor insira um formato válido.'),
            code='invalid'
        )  

def verify_roman(number):
    regex = re.compile(r'^M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3}$')

    if regex.match(number):
        return True

    return False

def check_exist_name(name):
    authors = Author.objects.filter(name__icontains=name)
    if authors.exists():
        raise ValidationError(
            ('Já existe esse pintor cadastrado. Procure por: %(value)s'),
            params={'value': authors.first()},
            code='invalid'
        )

def check_exist_church(name, city, state):
    churchs = Church.objects.filter(Q(
        Q(name__icontains=name) & Q(state__icontains=state) & Q(city__icontains=city)
    ))
    if churchs.exists():
        return churchs.first()
    return False
        
