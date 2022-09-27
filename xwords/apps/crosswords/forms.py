from django import forms
from django.core.exceptions import ValidationError
from django.contrib.postgres.forms import SimpleArrayField

from .models import Dictionary, Crossword

DIMENSIONS = [(a, a) for a in range(3, 36)]
BLOCKS = [(b, b) for b in range(0, 892)]


class CrosswordForm(forms.Form):
    crossword_choices = Dictionary.objects.filter(words__isnull=False).distinct().order_by('language')
    clues_choices = Dictionary.objects.all().order_by('language')
    language = forms.ModelChoiceField(label="Crossword Language: ", queryset=crossword_choices, required=True, initial="English")
    clues_language = forms.ModelChoiceField(label="Clues Language: ", queryset=clues_choices, required=True, initial="English")

    width = forms.ChoiceField(label="Width:", choices=DIMENSIONS, required=True, initial=10)
    height = forms.ChoiceField(label="Height:", choices=DIMENSIONS, required=True, initial=10)

    board = forms.CharField(max_length=1225, widget=forms.HiddenInput(), required=True)
    total_blocks = forms.ChoiceField(label="Number of Blocks:", choices=BLOCKS, required=True, initial=16)

    optional_words = SimpleArrayField(forms.CharField(max_length=256), widget=forms.HiddenInput(), required=False)

    def clean(self):
        cd = self.cleaned_data
        if 'language' not in cd:
            raise ValidationError("Field Crossword Language is required")
        if 'width' not in cd:
            raise ValidationError("Field Width is required")
        if 'height' not in cd:
            raise ValidationError("Field Height is required")
        if 'board' not in cd:
            raise ValidationError("Field Board is required")
        if 'total_blocks' not in cd:
            raise ValidationError("Field Number of Blocks is required")
        if 'optional_words' not in cd:
            cd['optional_words'] = list()
        cd['width'], cd['height'], cd['total_blocks'] = int(cd['width']), int(cd['height']), int(cd['total_blocks'])
        if cd['total_blocks'] + 9 > cd['height'] * cd['width']:
            raise ValidationError("Amount of blocks cannot exceed nine less than puzzle area!")
        if not cd['height'] % 2 and not cd['width'] % 2 and cd['total_blocks'] % 2:
            raise ValidationError("Amount of blocks cannot be odd for puzzles with two even dimensions!")
        if 'board' in cd and cd['total_blocks'] < cd['board'].count('#'):
            raise ValidationError("There are more blocks in the interactive board than in you requested!")
        return cd


class PDFForm(forms.Form):
    title = forms.CharField(label="Title", max_length=None, required=False,
                            widget=forms.TextInput(attrs={"class": "form-control"}))
    crossword = forms.ModelChoiceField(queryset=Crossword.objects.all(), widget=forms.HiddenInput())
    solution = forms.BooleanField(label="Print Solution:", required=False)
