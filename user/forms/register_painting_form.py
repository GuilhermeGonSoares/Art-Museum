

from django import forms
from museum.models import Author, Church, Engraving, Painting
from utils.django_form import date_validade


class RegisterPaintingForm(forms.ModelForm):
    name = forms.CharField(
        required=True,
        min_length=4,
        max_length=50,
        label="Nome",
        widget=forms.TextInput(attrs={
            'placeholder': 'Nome da pintura'
        })
    )

    summary = forms.CharField(
        required=False,
        min_length=10,
        max_length=350,
        label='Resumo',
        widget=forms.Textarea(attrs={
            'placeholder': 'Breve resumo da obra',
            'class': 'span-2'
        })
    )


    author = forms.ModelMultipleChoiceField(
        required=False,
        label="Pintor",
        queryset = Author.objects.all(),
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
            'cover': 'Imagem'
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



class RegisterAuthorForm(forms.ModelForm):

    name = forms.CharField(
        min_length=4,
        max_length=50, 
        required=True,
        label='Nome:',
        widget=forms.TextInput(attrs={
            'placeholder': 'Nome do pintor'
        })
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
    
    class Meta:
        model = Church
        fields = [
            'name',
            'city',
            'state',
        ]

class RegisterEngravingForm(forms.ModelForm):

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
