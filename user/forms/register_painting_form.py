

from collections import defaultdict

from django import forms
from django.core.exceptions import ValidationError
from pyUFbr.baseuf import ufbr

from museum.models import Author, Church, Engraving, Painting
from utils.django_form import (check_exist_church, check_exist_name,
                               date_validade)


#CADA CAMPO PODE TER UMA LISTA DE ERROS
#UTILIZANDO O defaultdict PARA JA DEIXAR O VALOR DA CHAVE=[] POR DEFAULT
#COM O DICIONÁRIO DE ERROS NOS CONSEGUIMOS MANDAR TODOS OS ERROS DE UMA VEZ PARA O USUÁRIO
class RegisterPaintingForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 
        self.__erros = defaultdict(list)
    
    name = forms.CharField(
        required=True,
        min_length=4,
        max_length=50,
        label="Nome da obra",
        widget=forms.TextInput(attrs={
            'placeholder': 'Nome da pintura'
        })
    )

    summary = forms.CharField(
        required=False,
        min_length=10,
        max_length=350,
        label='Intertexto',
        widget=forms.Textarea(attrs={
            'placeholder': 'Breve resumo da obra',
            'class': 'span-2'
        })
    )


    author = forms.ModelMultipleChoiceField(
        required=False,
        label="Pintor",
        queryset = Author.objects.filter(is_engraving=False),
        help_text='É permitido selecionar nenhum ou mais de um pintor',
        
    )
    
    church = forms.ModelChoiceField(
        required=False,
        label="Igreja",
        empty_label="Desconhecida",
        help_text="Selecione uma",
        queryset=Church.objects.all(),
        widget=forms.Select(),

    )

    date = forms.CharField(
        required = False,
        label="Data da obra",
        help_text = "Formato: \
            dia/mês/ano, \
            mês/ano, \
            ano ou \
            século(em romano)",
        widget=forms.TextInput(attrs={
            'placeholder': 'Ex: 28/01/1998, 01/1998, 1998, XX'
        }),
        validators=[date_validade]
    )
    
    class Meta:
        model = Painting
        fields = [
            'name',
            'date',
            'author',
            'engraving',
            'church',
            'summary',
            'description',
            'cover',
        ]
        labels = {
            'description': 'Descrição',
            'cover': 'Imagem',
            'engraving': 'Gravuras',
        }
        widgets = {
            'description': forms.Textarea(attrs={
                'class': 'span-2',
                'placeholder': 'Descrição detalhada da obra'
            }),
            'cover': forms.FileInput(attrs={
                'class': 'span-2'
            })
        }
    def clean(self):
        super_clean = super().clean()
        cleaned_data = self.cleaned_data
        name = cleaned_data.get('name')
        summary = cleaned_data.get('summary')
        
        if name == summary:
            self.__erros['summary'].append('Resumo não pode ser igual ao nome da obra')

        if self.__erros:
            raise ValidationError(self.__erros)

        return super_clean



class RegisterAuthorForm(forms.ModelForm):

    name = forms.CharField(
        min_length=4,
        max_length=50, 
        required=True,
        label='Nome:',
        widget=forms.TextInput(attrs={
            'placeholder': 'Nome do pintor'
        }),
        validators=[check_exist_name]
    )
    biography = forms.CharField(
        required=False,
        min_length=10,
        max_length=500,
        label='Biografia',
        widget=forms.Textarea(attrs={
            'class': 'span-2',
            'placeholder': 'Biografia'
        })
    )
    class Meta:
        model = Author
        fields = [
            'name',
            'biography'
        ]
    
    
        

class RegisterChurchForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 
        self.__erros_church = defaultdict(list)

    name = forms.CharField(
        min_length=4,
        max_length=100,
        required=True,
        label='Nome',
        widget=forms.TextInput(attrs={
            'placeholder': 'Nome da igreja'
        }),
        help_text='Nome da igreja que a pintura se encontra.'
    )


    class Meta:
        model = Church
        fields = [
            'name',
            'state',
            'city',
        ]
        labels={
            'state': 'Estado',
            'city': 'Cidade'
        }
        widgets={
            'state': forms.Select(
                choices=(
                    (None, '-- Selecione o estado --'), ('AC', 'AC'),('AL', 'AL'), ('AP', 'AP'),
                    ('AM', 'AM'), ('BA', 'BA'), ('CE', 'CE'), ('DF', 'DF'), ('ES','ES'),
                    ('GO', 'GO'), ('MA', 'MA'), ('MT', 'MT'), ('MS', 'MS'),
                    ('MG', 'MG'), ('PA', 'PA'), ('PB', 'PB'), ('PR', 'PR'),
                    ('PE', 'PE'), ('PI', 'PI'), ('RJ', 'RJ'), ('RN', 'RN'),
                    ('RS', 'RS'), ('RO', 'RO'), ('RR', 'RR'), ('SC', 'SC'),
                    ('SP', 'SP'), ('SE', 'SE'), ('TO','TO')
                )
            ),
            'city': forms.Select(
                choices=(
                    (None, '-- Selecione a cidade --'),
                    
                ),
                attrs={
                    'class': 'esconder-campo'
                }
            )
        }
        help_texts={
            'state': 'Selecione o estado.',
            'city': 'Selecione a cidade.'

        }

    def clean(self):
        super_clean = super().clean()
        cd = self.cleaned_data
        name = cd.get('name')
        city = cd.get('city')
        state = cd.get('state')
        exist_church = check_exist_church(name, city, state)

        if city == '' or city is None:
            self.__erros_church['city'].append('Selecionar cidade é obrigatório')

        if exist_church is not False:
            self.__erros_church['name'].append(f'Igreja já cadastrada. Procure por: {exist_church}')

        cidades_desse_estado = ufbr.list_cidades(state)
        if city != '' and city not in cidades_desse_estado:
            self.__erros_church['city'].append('Essa cidade não pertence a esse estado')

        if self.__erros_church:
            raise ValidationError(self.__erros_church)

        return super_clean

    def clean_state(self):
        state = self.cleaned_data.get('state')
        states_list = ['AC', 'AL', 'AM', 'AP', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MG', 'MS', 'MT',
        'PA', 'PB', 'PE', 'PI', 'PR', 'RJ', 'RN', 'RO', 'RR', 'RS', 'SC', 'SE', 'SP', 'TO']
        
        if state not in states_list:
            self.__erros_church['state'].append('Selecione o estado válido.')

        return state

class RegisterEngravingForm(forms.ModelForm):
    name = forms.CharField(
        min_length=4,
        max_length=100,
        label='Nome',
        widget=forms.TextInput(attrs={
            'placeholder': 'Nome da gravura'
        }),
        help_text='Digite o nome da gravura'
    )

    book = forms.CharField(
        required=False,
        min_length=4,
        max_length=100,
        label='Livro',
        widget=forms.TextInput(attrs={
            'placeholder': 'Digite o nome do livro'
        }),
        help_text='Livro que contém a gravura'
    )

    author = forms.ModelMultipleChoiceField(
        required=False,
        label="Pintor",
        queryset = Author.objects.filter(is_engraving=True),
        help_text='É permitido selecionar nenhum ou mais de um pintor',
        
    )

    class Meta:
        model = Engraving
        fields = [
            'name',
            'book',
            'author',
            'cover',
        ]
        
        widgets = {
            'cover': forms.FileInput(attrs={
                'class': 'span-2'
            })
        }
