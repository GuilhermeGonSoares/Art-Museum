
from django import forms
from museum.models import Author, Church, Painting


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
        max_length=250,
        label='Resumo',
        widget=forms.TextInput(attrs={
            'placeholder': 'Breve resumo da obra',
            'class': 'span-2'
        })
    )


    author = forms.ModelMultipleChoiceField(
        required=False,
        queryset = Author.objects.all(),
        widget = forms.CheckboxSelectMultiple(attrs={
            'classe':'author-field'
        }),
    )

    class Meta:
        model = Painting
        fields = [
            'name',
            'date',
            'author',
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
