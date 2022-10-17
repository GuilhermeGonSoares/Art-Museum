
from django import forms
from museum.models import Author, Church, Painting


class RegisterPaintingForm(forms.ModelForm):

    author = forms.ModelMultipleChoiceField(
        required=False,
        queryset = Author.objects.all(),
        widget = forms.CheckboxSelectMultiple(),
    )

    class Meta:
        model = Painting
        fields = [
            'name',
            'date',
            'summary',
            'description',
            'cover',
            'author',
            'church',
        ]
        widgets = {
            'description': forms.Textarea(attrs={
                'class': 'span-2'
            }),
            'cover': forms.FileInput(attrs={
                'class': 'span-2'
            })
        }

class RegisterAuthorForm(forms.ModelForm):

    name = forms.CharField(
        max_length=50, 
        required=True,
        label='Nome:',
        widget=forms.TextInput(attrs={
            'placeholder': 'Nome do pintor'
        })
    )
    biography = forms.CharField(
        required=False,
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
