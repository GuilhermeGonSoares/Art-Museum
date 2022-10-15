
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

    class Meta:
        model = Author
        fields = [
            'name',
        ]
